# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — a program's saved language and theme are read back as saved, a
value this version does not know is ignored, two programs never read each
other's choices, and every control of *Preferences* is read by its Save.

WHAT INVARIANT THIS PROTECTS, ported from OGR Slip2D (v0.1.486):

* ``tests/test_language_saved_v1289.py`` (v0.1.289, D290), the store only:
  nothing saved reads None; a saved language and theme are read back from
  the INI file under ``OGR_SETTINGS_DIR``; a stored value this version does
  not know is ignored. Its tests of ``apply_saved_preferences`` and of the
  main window (Spanish menus after a start, the notice of a language
  chosen) need Slip2D's ``__main__`` and window, and stay there;
* ``tests/test_preferences_controls_v1317.py`` (v0.1.317, D299): every
  control of the dialog that keeps a value is read by ``_accept``, on the
  source and on the real dialog; the three check boxes that changed nothing
  are gone; Save emits the language and the theme;
* ``tests/test_language_notice_v1291.py`` (v0.1.291, D290b): Save announces
  a language only when it changed.

What OGR GUI 0.1.0 changed: the module functions of Slip2D
(``saved_language()``, ``save_language()``…) are now the methods of a
``Preferences(application, file_stem)`` object, one per program, because
the program's name was a constant of Slip2D's module. New here: **two
programs' Preferences never read each other's values**, in the INI files
of the test folder and in the names of the user's store (``QSettings`` of
the organisation and the program), and nothing is kept in the object.

Each test gives ``OGR_SETTINGS_DIR`` a folder of its own and puts back the
variable, the language and the folder in ``finally`` (rule 5): the runner
counts the files of its own settings folder in its leak check.
"""
from __future__ import annotations

import ast
import os
import shutil
import tempfile
from pathlib import Path

import pytest

_SRC = (Path(__file__).resolve().parent.parent / "ogr_ui" / "dialogs"
        / "preferences_dialog.py")
_VALUE_WIDGETS = ("QCheckBox", "QComboBox", "QSpinBox", "QDoubleSpinBox",
                  "QLineEdit", "QRadioButton", "QSlider")
_GONE = ("Show Tabs for Multiple Windows",
         "Mark file as modified after importing",
         "Default to compressed format when saving")


def _app():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


class _Fresh:
    """A preferences folder of the test's own; everything put back."""

    def __enter__(self):
        from ogr_ui.i18n import current_language
        self.env = os.environ.get("OGR_SETTINGS_DIR")
        self.lang = current_language()
        self.dir = tempfile.mkdtemp(prefix="ogr_ui_test_prefs_")
        os.environ["OGR_SETTINGS_DIR"] = self.dir
        return self

    def __exit__(self, *exc):
        from ogr_ui.i18n import set_language
        set_language(self.lang)
        if self.env is None:
            os.environ.pop("OGR_SETTINGS_DIR", None)
        else:
            os.environ["OGR_SETTINGS_DIR"] = self.env
        shutil.rmtree(self.dir, ignore_errors=True)
        return False


def _prefs(name="OGR Slip2D", stem="ogr-slip2d"):
    from ogr_ui.user_prefs import Preferences
    return Preferences(name, stem)


# ======================================================================
class TestTheStore:

    def test_nothing_saved_reads_none(self):
        with _Fresh():
            p = _prefs()
            assert p.saved_language() is None
            assert p.saved_theme() is None

    def test_a_saved_choice_is_read_back(self):
        with _Fresh() as f:
            p = _prefs()
            p.save_language("es")
            p.save_theme("dark")
            assert p.saved_language() == "es"
            assert p.saved_theme() == "dark"
            assert os.listdir(f.dir) == ["ogr-slip2d.ini"]
            # and changed again
            p.save_language("en")
            p.save_theme("light")
            assert (p.saved_language(), p.saved_theme()) == ("en", "light")

    def test_an_unknown_value_is_ignored(self):
        from PySide6.QtCore import QSettings
        with _Fresh() as f:
            s = QSettings(os.path.join(f.dir, "ogr-slip2d.ini"),
                          QSettings.Format.IniFormat)
            s.setValue("language", "tlh")
            s.setValue("theme", "neon")
            s.sync()
            del s
            p = _prefs()
            assert p.saved_language() is None
            assert p.saved_theme() is None

    def test_nothing_is_kept_in_the_object(self):
        """Every call reads the store: what another object of the same
        program saved is read at once."""
        with _Fresh():
            reader, writer = _prefs(), _prefs()
            assert reader.saved_language() is None
            writer.save_language("es")
            assert reader.saved_language() == "es"

    def test_a_program_needs_its_name_and_its_file(self):
        from ogr_ui.user_prefs import Preferences
        for name, stem in (("", "ogr-x"), ("OGR X", ""), (None, "ogr-x")):
            with pytest.raises(ValueError):
                Preferences(name, stem)

    def test_without_the_folder_it_is_the_users_store_of_the_program(self):
        """Without ``OGR_SETTINGS_DIR``: ``QSettings`` of the suite's
        organisation and the program's name. Read only: nothing is written
        to the user's store."""
        from PySide6.QtCore import QSettings

        from ogr_ui.user_prefs import ORGANIZATION
        env = os.environ.pop("OGR_SETTINGS_DIR", None)
        try:
            s = _prefs("OGR FEM2D", "ogr-fem2d").settings()
            assert s.format() == QSettings.Format.NativeFormat
            assert s.organizationName() == ORGANIZATION == "OpenGeoRock Suite"
            assert s.applicationName() == "OGR FEM2D"
        finally:
            if env is not None:
                os.environ["OGR_SETTINGS_DIR"] = env

    def test_with_the_folder_it_is_the_programs_ini_file(self):
        from PySide6.QtCore import QSettings
        with _Fresh() as f:
            s = _prefs("OGR FEM2D", "ogr-fem2d").settings()
            assert s.format() == QSettings.Format.IniFormat
            assert Path(s.fileName()) == Path(f.dir) / "ogr-fem2d.ini"


class TestTwoPrograms:
    """New in OGR GUI 0.1.0: each program makes its own Preferences."""

    def test_they_never_read_each_others_values(self):
        with _Fresh() as f:
            slip, fem = _prefs("OGR Slip2D", "ogr-slip2d"), \
                _prefs("OGR FEM2D", "ogr-fem2d")
            slip.save_language("es")
            slip.save_theme("dark")
            assert fem.saved_language() is None
            assert fem.saved_theme() is None
            fem.save_language("en")
            fem.save_theme("light")
            assert (slip.saved_language(), slip.saved_theme()) == \
                ("es", "dark")
            assert (fem.saved_language(), fem.saved_theme()) == \
                ("en", "light")
            assert sorted(os.listdir(f.dir)) == ["ogr-fem2d.ini",
                                                 "ogr-slip2d.ini"]

    def test_in_the_users_store_they_are_two_keys(self):
        env = os.environ.pop("OGR_SETTINGS_DIR", None)
        try:
            a = _prefs("OGR Slip2D", "ogr-slip2d").settings()
            b = _prefs("OGR FEM2D", "ogr-fem2d").settings()
            assert a.organizationName() == b.organizationName()
            assert a.applicationName() != b.applicationName()
            assert a.fileName() != b.fileName()
        finally:
            if env is not None:
                os.environ["OGR_SETTINGS_DIR"] = env


# ======================================================================
def _methods():
    tree = ast.parse(_SRC.read_text(encoding="utf-8"))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef)
               and n.name == "PreferencesDialog")
    return {n.name: n for n in cls.body if isinstance(n, ast.FunctionDef)}


def _created(fn):
    """``self.<attr>`` assigned a value widget in ``fn``."""
    out = set()
    for n in ast.walk(fn):
        if (isinstance(n, ast.Assign) and isinstance(n.value, ast.Call)
                and getattr(n.value.func, "id", None) in _VALUE_WIDGETS):
            for t in n.targets:
                if (isinstance(t, ast.Attribute)
                        and isinstance(t.value, ast.Name)
                        and t.value.id == "self"):
                    out.add(t.attr)
    return out


def _read(fn):
    """``self.<attr>`` mentioned anywhere in ``fn``."""
    return {n.attr for n in ast.walk(fn)
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
            and n.value.id == "self"}


def _dialog(active_theme="light"):
    from ogr_ui.dialogs.preferences_dialog import PreferencesDialog
    _app()
    return PreferencesDialog(active_theme=active_theme)


def _saved(lang_in_session, choose_language=None, choose_theme="dark"):
    """Open Preferences with ``lang_in_session`` active, pick, press Save;
    returns (languages emitted, themes emitted)."""
    from ogr_ui.i18n import current_language, set_language
    prev = current_language()
    langs, themes = [], []
    dlg = None
    try:
        set_language(lang_in_session)
        dlg = _dialog()
        dlg.language_changed.connect(langs.append)
        dlg.theme_changed.connect(themes.append)
        if choose_language is not None:
            dlg.cbo_language.setCurrentIndex(
                dlg.cbo_language.findData(choose_language))
        dlg.cbo_theme.setCurrentIndex(dlg.cbo_theme.findData(choose_theme))
        dlg._accept()
    finally:
        set_language(prev)
        if dlg is not None:
            dlg.deleteLater()
    return langs, themes


class TestEveryControlHasAReader:
    """test_preferences_controls_v1317 (rule 7)."""

    def test_in_the_source(self):
        methods = _methods()
        created = _created(methods["__init__"])
        assert created == {"cbo_language", "cbo_theme"}, created
        unread = created - _read(methods["_accept"])
        assert unread == set(), unread

    def test_in_the_real_dialog(self):
        from PySide6.QtWidgets import (QAbstractSpinBox, QCheckBox,
                                       QComboBox, QLineEdit, QRadioButton,
                                       QSlider)
        d = _dialog()
        try:
            read = [getattr(d, a) for a in _read(_methods()["_accept"])
                    if hasattr(d, a)]
            values = [w for cls in (QCheckBox, QComboBox, QAbstractSpinBox,
                                    QLineEdit, QRadioButton, QSlider)
                      for w in d.findChildren(cls)
                      # a combo's own editor is part of the combo
                      if not isinstance(w.parent(), QComboBox)]
            assert values
            for w in values:
                assert any(w is r for r in read), type(w).__name__
        finally:
            d.deleteLater()

    def test_the_three_check_boxes_are_gone(self):
        from PySide6.QtWidgets import QCheckBox
        d = _dialog()
        try:
            texts = [c.text() for c in d.findChildren(QCheckBox)]
            for gone in _GONE:
                assert gone not in texts
        finally:
            d.deleteLater()

    def test_it_offers_every_language_and_theme_and_opens_on_the_active(self):
        from ogr_ui.i18n import available_languages, current_language
        from ogr_ui.themes import THEMES
        d = _dialog(active_theme="dark")
        try:
            langs = [d.cbo_language.itemData(i)
                     for i in range(d.cbo_language.count())]
            themes = [d.cbo_theme.itemData(i)
                      for i in range(d.cbo_theme.count())]
            assert langs == available_languages()
            assert themes == list(THEMES)
            assert d.cbo_language.currentData() == current_language()
            assert d.cbo_theme.currentData() == "dark"
            # each language by its own name
            names = {d.cbo_language.itemData(i): d.cbo_language.itemText(i)
                     for i in range(d.cbo_language.count())}
            assert names["en"] == "English" and names["es"] == "Español"
        finally:
            d.deleteLater()

    def test_an_unknown_active_theme_opens_on_the_first(self):
        d = _dialog(active_theme="neon")
        try:
            assert d.cbo_theme.currentIndex() == 0
        finally:
            d.deleteLater()


class TestWhatSaveSays:
    """test_preferences_controls_v1317 (control) and
    test_language_notice_v1291 (D290b)."""

    def test_save_emits_the_language_and_the_theme(self):
        langs, themes = _saved("en", choose_language="es",
                               choose_theme="dark")
        assert (langs, themes) == (["es"], ["dark"])

    def test_a_theme_change_does_not_announce_a_language(self):
        langs, themes = _saved("en")
        assert langs == []
        assert themes == ["dark"]

    def test_another_language_is_announced(self):
        langs, _themes = _saved("en", choose_language="es")
        assert langs == ["es"]

    def test_saving_spanish_as_it_is_says_nothing(self):
        langs, themes = _saved("es", choose_theme="light")
        assert langs == []
        assert themes == ["light"]

    def test_in_spanish_it_speaks_spanish(self):
        from PySide6.QtWidgets import QGroupBox

        from ogr_ui.i18n import current_language, set_language
        prev = current_language()
        d = None
        try:
            set_language("es")
            d = _dialog()
            assert d.windowTitle() == "Preferencias"
            assert [g.title() for g in d.findChildren(QGroupBox)] == \
                ["Interfaz"]
            assert [d.cbo_theme.itemText(i)
                    for i in range(d.cbo_theme.count())] == ["Claro",
                                                             "Oscuro"]
        finally:
            set_language(prev)
            if d is not None:
                d.deleteLater()
