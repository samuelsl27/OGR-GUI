# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — Qt's own texts (the standard buttons «Yes», «No», «Save»,
«Cancel»…) follow the language, and a switch of language replaces Qt's
catalogue instead of piling one on another.

WHAT INVARIANT THIS PROTECTS, ported from OGR Slip2D (v0.1.486):

* ``tests/test_qt_translations_v1292.py`` (v0.1.292, D302):
  ``install_qt_translator(app, "es")`` loads ``qtbase_es.qm``, so a message
  box's Yes is «&Sí» and a button box's Save «Guardar»; English loads
  nothing; once removed, the buttons are English again. Its test of
  ``apply_saved_preferences`` needs Slip2D's ``__main__`` and stays there;
* the ``qt_catalog`` part of ``tests/test_console_language_demo_v1329.py``
  (v0.1.329, D327): ``switch_qt_translator`` puts the new catalogue in
  place of the one it installed before, so ``reset_qt_translator`` leaves
  English. Its test of the notice «Language changed…» needs the main
  window and stays in Slip2D.

Added here: a language Qt has no catalogue for installs nothing, and
``reset_qt_translator`` with nothing installed is a no-op.

No message box is opened: ``_yes()`` builds one and reads its button. Every
catalogue installed here is removed in ``finally``, through
``reset_qt_translator`` when ``switch_qt_translator`` installed it, so that
``ogr_ui.qt_catalog._CURRENT`` is None again (rule 5).
"""
from __future__ import annotations


def _app():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


def _yes():
    from PySide6.QtWidgets import QMessageBox
    _app()
    box = QMessageBox(QMessageBox.Question, "t", "x",
                      QMessageBox.Yes | QMessageBox.No)
    try:
        return box.button(QMessageBox.Yes).text()
    finally:
        box.deleteLater()


def _remove(app, translator):
    if translator is not None:
        app.removeTranslator(translator)
        translator.deleteLater()


class TestTheCatalogue:

    def test_spanish_translates_the_standard_buttons(self):
        from PySide6.QtWidgets import QDialogButtonBox

        from ogr_ui.qt_catalog import install_qt_translator
        app = _app()
        t = install_qt_translator(app, "es")
        try:
            assert t is not None
            assert _yes() == "&Sí"
            bb = QDialogButtonBox(QDialogButtonBox.Save
                                  | QDialogButtonBox.Cancel)
            try:
                assert bb.button(QDialogButtonBox.Save).text() == "Guardar"
                assert bb.button(QDialogButtonBox.Cancel).text() == \
                    "Cancelar"
            finally:
                bb.deleteLater()
        finally:
            _remove(app, t)
        assert _yes() == "&Yes"

    def test_english_loads_nothing(self):
        from ogr_ui.qt_catalog import install_qt_translator
        assert install_qt_translator(_app(), "en") is None
        assert install_qt_translator(_app(), "") is None
        assert _yes() == "&Yes"

    def test_a_language_without_a_catalogue_loads_nothing(self):
        from ogr_ui.qt_catalog import install_qt_translator, switch_qt_translator
        import ogr_ui.qt_catalog as qc
        app = _app()
        try:
            assert install_qt_translator(app, "tlh") is None
            assert switch_qt_translator(app, "tlh") is None
            assert qc._CURRENT is None
            assert _yes() == "&Yes"
        finally:
            qc.reset_qt_translator(app)

    def test_install_leaves_the_switch_alone(self):
        """``install_qt_translator`` is the caller's to remove: it does not
        become the one ``switch_qt_translator`` replaces."""
        import ogr_ui.qt_catalog as qc
        app = _app()
        t = qc.install_qt_translator(app, "es")
        try:
            assert qc._CURRENT is None
        finally:
            _remove(app, t)


class TestTheSwitch:

    def test_a_switch_replaces_and_does_not_pile_up(self):
        import ogr_ui.qt_catalog as qc
        app = _app()
        try:
            first = qc.switch_qt_translator(app, "es")
            second = qc.switch_qt_translator(app, "es")
            assert first is not None and second is not None
            assert first is not second
            assert qc._CURRENT is second
            qc.reset_qt_translator(app)
            # had the first one stayed, the Spanish would still be there
            assert _yes() == "&Yes"
            assert qc._CURRENT is None
        finally:
            qc.reset_qt_translator(app)

    def test_spanish_then_english(self):
        import ogr_ui.qt_catalog as qc
        app = _app()
        try:
            assert qc.switch_qt_translator(app, "es") is not None
            assert _yes() == "&Sí"
            assert qc.switch_qt_translator(app, "en") is None
            assert _yes() == "&Yes"
            assert qc._CURRENT is None
        finally:
            qc.reset_qt_translator(app)

    def test_reset_with_nothing_installed_is_a_no_op(self):
        import ogr_ui.qt_catalog as qc
        app = _app()
        assert qc._CURRENT is None
        qc.reset_qt_translator(app)
        assert qc._CURRENT is None
        assert _yes() == "&Yes"
