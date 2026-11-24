# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — ``ogr_ui`` imports neither the core nor any program, read from the
source and measured at run time.

The pieces of this package come from OGR Slip2D's interface (``ogr_gui``,
v0.1.486), where they sat next to the limit-equilibrium engine and the
core's ``Project``: three of them imported the core (the snap engine its
``Boundary`` and ``Vertex``, the background tasks its progress and its
``save_results``) and two imported modules of that program (the snap
dialog its data tips, the background tasks its dialogs and its messages).
On the way out each was cut to a small interface of its own (their
docstrings say which). This file keeps them cut.

Why the core too, and not only the programs: a program pins its own tag of
the core, and pip refuses two different git references to the same
distribution. Had this package imported ``ogr_core`` it would have had to
depend on it, and every program would have had to pin the core this package
pins (the owner's decision of 2026-11-24). ``ogr_core`` is only the runner of
this repository's tests (``tests/_runner.py``), never ``ogr_ui``'s.

The invariants:

* **the census is exact**: every import in ``ogr_ui`` of the core
  (``ogr_core``), of a program or its layers (``ogr_slip2d``, ``ogr_fem2d``,
  ``ogr_data``, ``ogr_gui`` — Slip2D's interface —, ``ogr_api``,
  ``ogr_cli``, ``ogr_mcp``), of the MCP SDK (``mcp``), every ``importlib``
  and every ``__import__`` call, inside functions and classes too, is an
  entry of :data:`ALLOWED` (none today). A new one fails, and so does an
  entry that matches nothing;
* **the census sees what it must**: a module written here with one import
  of each kind is found whole;
* **it looked at something**: it read the package's ``__init__``;
* **at run time**: in a fresh interpreter, importing every module of
  ``ogr_ui`` and building the widgets that read other modules (a theme
  applied, a status bar, a legend, the snap and contour dialogs, a task run)
  leaves none of those packages in ``sys.modules``.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

#: The core, the programs and their layers, the MCP SDK, and the two ways
#: around an import statement.
BANNED = frozenset({"ogr_core", "ogr_slip2d", "ogr_fem2d", "ogr_data",
                    "ogr_gui", "ogr_api", "ogr_cli", "ogr_mcp", "mcp",
                    "importlib"})
DYNAMIC = "__import__"

#: ``(file, enclosing function, module)``: how many times it is written.
ALLOWED: Counter = Counter()


def census_of(path: Path, root: Path) -> Counter:
    """The banned imports of one file, by enclosing function."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    rel = path.relative_to(root).as_posix()
    found: Counter = Counter()

    def visit(node, where):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef,
                                  ast.ClassDef)):
                visit(child, where + [child.name])
                continue
            modules = []
            if isinstance(child, ast.Import):
                modules = [a.name.split(".")[0] for a in child.names]
            elif (isinstance(child, ast.ImportFrom) and child.level == 0
                  and child.module):
                modules = [child.module.split(".")[0]]
            elif (isinstance(child, ast.Call)
                  and isinstance(child.func, ast.Name)
                  and child.func.id == DYNAMIC):
                modules = [DYNAMIC]
            for module in modules:
                if module in BANNED or module == DYNAMIC:
                    found[(rel, ".".join(where) or "<module>", module)] += 1
            visit(child, where)

    visit(tree, [])
    return found


def _package_files() -> list:
    return sorted(p for p in (_ROOT / "ogr_ui").rglob("*.py")
                  if "__pycache__" not in p.parts)


def package_census() -> Counter:
    found: Counter = Counter()
    for path in _package_files():
        found.update(census_of(path, _ROOT))
    return found


class TestThePackageImportsNoCoreAndNoProgram:

    def test_the_census_is_the_allowed_list_exactly(self):
        found = package_census()
        new = found - ALLOWED
        gone = ALLOWED - found
        assert not new, ("imports of the core or of a program", new)
        assert not gone, ("entries that match nothing any more: delete "
                          "them", gone)

    def test_the_census_looked_at_the_package(self):
        names = {p.relative_to(_ROOT).as_posix() for p in _package_files()}
        for expected in ("ogr_ui/__init__.py", "ogr_ui/canvas/snap_engine.py",
                         "ogr_ui/background.py", "ogr_ui/testing/texts.py"):
            assert expected in names, expected

    def test_the_census_sees_every_kind_of_import(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pkg = root / "ogr_ui" / "x"
            pkg.mkdir(parents=True)
            (pkg / "m.py").write_text(
                "from __future__ import annotations\n"
                "from typing import TYPE_CHECKING\n"
                "import os\n"
                "from . import sibling\n"
                "from PySide6.QtWidgets import QWidget\n"
                "if TYPE_CHECKING:\n"
                "    from ogr_core.geometry import Boundary\n"
                "class K:\n"
                "    def f(self):\n"
                "        import ogr_slip2d.search as m\n"
                "        return __import__('ogr_fem2d')\n"
                "def g():\n"
                "    import importlib\n"
                "    from ogr_gui.data_tips import DataTipMode\n"
                "    import ogr_data, mcp\n",
                encoding="utf-8")
            found = census_of(pkg / "m.py", root)
        assert found == Counter({
            ("ogr_ui/x/m.py", "<module>", "ogr_core"): 1,
            ("ogr_ui/x/m.py", "K.f", "ogr_slip2d"): 1,
            ("ogr_ui/x/m.py", "K.f", DYNAMIC): 1,
            ("ogr_ui/x/m.py", "g", "importlib"): 1,
            ("ogr_ui/x/m.py", "g", "ogr_gui"): 1,
            ("ogr_ui/x/m.py", "g", "ogr_data"): 1,
            ("ogr_ui/x/m.py", "g", "mcp"): 1,
        }), found


#: Run in a fresh interpreter: every module imported, and the pieces that
#: reach other modules when they are built, built.
_PROBE = r"""
import json, pkgutil, sys
sys.path.insert(0, sys.argv[1])
import importlib
import ogr_ui
for m in pkgutil.walk_packages(ogr_ui.__path__, "ogr_ui."):
    importlib.import_module(m.name)
from PySide6.QtWidgets import QApplication, QMainWindow
app = QApplication.instance() or QApplication([])
from ogr_ui.themes import apply_theme
from ogr_ui.resources.icons import icon
from ogr_ui.widgets.status_bar import OgrStatusBar
from ogr_ui.widgets.legend import ColourScaleLegend
from ogr_ui.dialogs.snap_dialog import SnapDialog
from ogr_ui.dialogs.contour_options_dialog import ContourOptionsDialog
from ogr_ui.canvas.snap_engine import SnapEngine, SnapSettings, SnapShape, SnapPoint
from ogr_ui.contours import ContourField, ContourSettings, RangePreset
from ogr_ui.background import run_task
from ogr_ui.user_prefs import Preferences
apply_theme(app, "dark"); apply_theme(app, "light")
icon("save")
w = QMainWindow(); w.setStatusBar(OgrStatusBar(w))
ColourScaleLegend()
SnapDialog(SnapSettings())
ContourOptionsDialog(ContourSettings(field="h"),
                     fields=[ContourField("h", "Total head")],
                     presets=[RangePreset("0 to 6", 0.0, 6.0, 24)])
SnapEngine().resolve(SnapPoint(0, 0), [SnapShape.polyline([SnapPoint(0, 0), SnapPoint(1, 0)])])
run_task(w, lambda cb: 1)
Preferences("OGR Test", "ogr-test").saved_theme()
banned = sys.argv[2].split(",")
print(json.dumps(sorted(k for k in sys.modules if k.split(".")[0] in banned)))
"""


class TestAtRunTime:

    def test_nothing_of_the_core_or_of_a_program_is_loaded(self):
        banned = sorted(BANNED - {"importlib"})
        env = dict(os.environ)
        env["QT_QPA_PLATFORM"] = "offscreen"
        with tempfile.TemporaryDirectory() as tmp:
            env["OGR_SETTINGS_DIR"] = tmp
            out = subprocess.run(
                [sys.executable, "-c", _PROBE, str(_ROOT), ",".join(banned)],
                capture_output=True, text=True, env=env, timeout=120)
        assert out.returncode == 0, out.stderr[-2000:]
        loaded = json.loads(out.stdout.strip().splitlines()[-1])
        assert loaded == [], loaded
