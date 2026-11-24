# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
The test runner of OGR GUI: the suite's runner
(``ogr_core.testing.runner``), pointed at this repository.

    QT_QPA_PLATFORM=offscreen python tests/_runner.py            # everything; what CI runs
    QT_QPA_PLATFORM=offscreen python tests/_runner.py snap       # files whose name contains it
    QT_QPA_PLATFORM=offscreen python tests/_runner.py -k legend  # tests whose name contains it
    QT_QPA_PLATFORM=offscreen python tests/_runner.py --jobs 4   # in four processes

``ogr_core`` is not a dependency of ``ogr_ui``: it is here for its runner and
its leak check only, and comes from the tag the ``test`` extra of
``pyproject.toml`` pins, installed, never from a tree. The header of every
run names it (``shared: ogr_core X.Y.Z …``), and the runner refuses another
version. ``--dev-core`` accepts a development core of a later release, as in
the programs.

What the configuration below says of this repository: its package, the
core it borrows the runner from, the hooks Qt needs (the garbage guard and
the windows left alive, as OGR Slip2D's runner), the settings folder every
run gets (so no test reads the user's preferences), and its part of the
leak check's allow-list.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_TESTS = Path(__file__).resolve().parent
_ROOT = _TESTS.parent
# This tree first, before any editable install can answer for it (see
# foreign_packages in the runner).
sys.path.insert(0, str(_ROOT))

from ogr_core.testing import leaks, runner  # noqa: E402

#: The package this repository contains, and the one it takes its runner from.
OWN = ("ogr_ui",)
SHARED = ("ogr_core",)
#: The name this repository's durations are kept under on the machine.
LABEL = "ogr-gui"
#: The folder every run gets, empty and of its own: the saved preferences
#: (ogr_ui.user_prefs reads OGR_SETTINGS_DIR).
RUN_FOLDERS = {"OGR_SETTINGS_DIR": "settings"}

#: This repository's part of the leak check's allow-list; the suite's own is
#: in ``ogr_core.testing.leaks.ALLOWED``. Every entry says why. They are the
#: entries OGR Slip2D's runner has for these same modules.
ALLOWED = (
    leaks.Allow("mod:*.icon", leaks.ANY,
                "ogr_ui.resources.icons.icon, an lru_cache of icons, under "
                "every module that imports it; a change of theme empties it "
                "on purpose"),
    leaks.Allow("mod:ogr_ui.gc_guard._kept", leaks.ANY,
                "garbage the collector found on another thread, waiting to "
                "be freed on the main one: the runner frees it before every "
                "file"),
    leaks.Allow("mod:ogr_ui.wheel_guard._guard", leaks.INSTALLED,
                "the wheel guard, installed once in the application by the "
                "program's first window; a test that installs it puts back "
                "what it found (test_dialog_guards_v010)"),
    leaks.Allow("mod:ogr_ui.button_floor._floor", leaks.INSTALLED,
                "the button floor, installed in the application by the "
                "first theme applied"),
    leaks.Allow("mod:ogr_ui.themes._ORIGINAL_PALETTE", leaks.INSTALLED,
                "the application's palette, captured the first time a theme "
                "is applied, to go back to"),
    leaks.Allow("mpl.rcParams",
                leaks.from_value("[]", to="['backend_fallback']"),
                "matplotlib.use(), which ogr_ui.xy_chart calls before its "
                "first chart, always sets backend_fallback to False "
                "(matplotlib/__init__.py). Only that key, and only from a "
                "clean rcParams: any other one changed is still a leak"),
)


def _install_gc_guard() -> None:
    # OGR Slip2D v0.1.302 (D310) — cyclic garbage found on a worker thread is
    # held for the main thread instead of handed to shiboken's deferred
    # deletion (ogr_ui/gc_guard.py). Called once the trees are checked: it
    # imports from the tree just checked.
    from ogr_ui import gc_guard
    gc_guard.install()


def _release_garbage() -> None:
    from ogr_ui import gc_guard
    gc_guard.release()


def _release_windows() -> int:
    """Delete the windows with no parent the tests left alive, with Python
    alive, before the interpreter's shutdown; returns how many (OGR Slip2D
    v0.1.422, D370: at shutdown PySide deletes every wrapped object one by
    one, in no order a window's children can rely on, and the suite
    segfaulted on Linux after its totals)."""
    if "PySide6.QtWidgets" not in sys.modules:
        return 0
    import shiboken6
    from PySide6.QtWidgets import QApplication
    app = QApplication.instance()
    if app is None:
        return 0
    released = 0
    for window in [w for w in app.topLevelWidgets() if w.parent() is None]:
        if shiboken6.isValid(window):
            shiboken6.delete(window)
            released += 1
    return released


HOOKS = runner.Hooks(before_run=_install_gc_guard,
                     before_file=_release_garbage,
                     after_run=_release_windows)


def pinned() -> dict:
    """``{"ogr_core": version}`` as the ``test`` extra of ``pyproject.toml``
    pins it: a git reference to a tag, or ``==``. The core's own
    ``pinned_from_pyproject`` reads the dependencies, where this package
    does not have it on purpose."""
    import tomllib
    data = tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    extras = data.get("project", {}).get("optional-dependencies", {})
    for req in extras.get("test", []):
        m = re.match(r"\s*ogr[-_.]core\s*(?:\[[^\]]*\])?\s*(.*)$", req, re.I)
        if not m:
            continue
        rest = m.group(1).split(";", 1)[0].strip()
        tag = re.match(r"@\s*\S+@v?(\d+(?:\.\d+)*)$", rest)
        exact = re.match(r"==\s*(\d+(?:\.\d+)*)$", rest)
        found = tag or exact
        return {"ogr_core": found.group(1)} if found else {}
    return {}


def config() -> dict:
    return {"own": OWN, "shared": SHARED, "pinned": pinned(), "hooks": HOOKS,
            "allowed": ALLOWED, "run_folders": RUN_FOLDERS, "label": LABEL}


def main(patterns=(), k=None, list_only=False, **options) -> int:
    """This repository's run, for a test that wants to drive it."""
    return runner.main(_TESTS, patterns, k, list_only, **config(), **options)


if __name__ == "__main__":
    if not pinned():
        print("pyproject.toml does not pin ogr-core in its 'test' extra to "
              "a tag or an exact version: nothing to check the runner's "
              "core against.")
        sys.exit(2)
    sys.exit(runner.cli(_TESTS, **config()))
