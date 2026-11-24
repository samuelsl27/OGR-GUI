# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.289 (D290) — the application preferences that outlive a session: the
language and the theme.

Until this version *Preferences* changed the language for the session and
said «Restart the application to fully apply translations»; nothing stored
the choice, so the restart came back in English and the advice was false.
The menus, the toolbar and the status bar are built once, with ``tr()``, so
the language has to be set BEFORE the window is built: ``ogr_ui.__main__``
asks this module first thing (the owner's decision: save and restart, no
live retranslation).

Where it is kept: ``QSettings("OpenGeoRock Suite", <the program's name>)``
— the user's registry on Windows, a local file elsewhere; nothing leaves the
machine. If ``OGR_SETTINGS_DIR`` is set, an INI file in that folder instead:
the test runner points it at an empty folder of its own, so no test ever
reads or writes the user's preferences (rule 5).

A stored value this version does not know (a language or a theme that no
longer exists) is ignored, not trusted.

**OGR GUI 0.1.0.** In OGR Slip2D the program's name was a constant of this
module (``"OGR Slip2D"``, and ``ogr-slip2d.ini`` under the test folder).
Here each program makes its own :class:`Preferences` with its name, so two
programs of the suite never read each other's choices.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import os
from typing import Optional

from PySide6.QtCore import QSettings

ORGANIZATION = "OpenGeoRock Suite"


class Preferences:
    """The saved preferences of one program.

    ``application`` is its name in ``QSettings`` (``"OGR FEM2D"``);
    ``file_stem`` names the INI file under ``OGR_SETTINGS_DIR``
    (``"ogr-fem2d"``). Nothing is kept in the object: every call reads or
    writes the store, as the module functions of OGR Slip2D did."""

    def __init__(self, application: str, file_stem: str) -> None:
        if not application or not file_stem:
            raise ValueError("a program's preferences need its name and "
                             "the stem of its file")
        self.application = application
        self.file_stem = file_stem

    def settings(self) -> QSettings:
        folder = os.environ.get("OGR_SETTINGS_DIR")
        if folder:
            return QSettings(os.path.join(folder, self.file_stem + ".ini"),
                             QSettings.Format.IniFormat)
        return QSettings(ORGANIZATION, self.application)

    def _read(self, key: str, allowed) -> Optional[str]:
        value = self.settings().value(key)
        return value if isinstance(value, str) and value in allowed else None

    def _write(self, key: str, value: str) -> None:
        s = self.settings()
        s.setValue(key, value)
        s.sync()

    def saved_language(self) -> Optional[str]:
        """The language chosen in a previous session, or None."""
        from .i18n import available_languages
        return self._read("language", available_languages())

    def save_language(self, code: str) -> None:
        self._write("language", code)

    def saved_theme(self) -> Optional[str]:
        """The theme chosen in a previous session, or None."""
        from .themes import THEMES
        return self._read("theme", THEMES)

    def save_theme(self, name: str) -> None:
        self._write("theme", name)
