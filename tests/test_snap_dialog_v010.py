# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.0 — the Snap dialog (``ogr_ui.dialogs.snap_dialog``), on its
own, with no main window.

The invariants:

* **one source of truth**: the dialog edits the snap settings object it is
  given, in place, on OK and only on OK, so the engine and the status-bar
  words that read that object never need a synchronisation step;
* **no setting does nothing** (rule 7): every control of the dialog moves
  the field of the settings it stands for, or the data-tip mode;
* *Restore Defaults* puts every control back to ``SnapSettings()`` and the
  data tips to *Maximum*; the combo offers the three
  :class:`~ogr_ui.data_tip_mode.DataTipMode` and opens on the one given;
* the tolerances say they are screen pixels, so nobody "fixes" them into
  metres;
* in Spanish, with either theme, at its minimum size the dialog cuts no
  button, label, check box or box, and fits a 1366 x 768 screen.

What changed on the way out of OGR Slip2D: ``DataTipMode`` comes from
``ogr_ui.data_tip_mode`` (Slip2D's ``ogr_gui/data_tips.py``, which also
builds the tips and stayed in that program).

Ported from OGR Slip2D (v0.1.486):

* ``tests/test_m1_datatips_snap_v151.py`` (v0.1.51, phase M1),
  ``TestSnapDialog``: every test but ``test_dialog_updates_the_status_words``,
  which drives Slip2D's main window; built here on a ``SnapSettings`` of
  the test's own instead of the main window's canvas. Its status-bar and
  keyboard classes need that window and stay in Slip2D.
* ``tests/test_dialogs_fit_v1315.py`` (v0.1.315, D293; v0.1.326, D319-D321):
  its census, for the one dialog of it that lives here, ``SnapDialog``.
  The rest of the census is Slip2D's dialogs.
"""
from __future__ import annotations

import contextlib

from PySide6.QtWidgets import QApplication

from ogr_ui.canvas.snap_engine import SnapSettings
from ogr_ui.data_tip_mode import DataTipMode

_MISSING = object()
_SCREEN = (1366, 728)          # 768 less a taskbar


def _app():
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _english():
    from ogr_ui.i18n import current_language, set_language
    language = current_language()
    try:
        set_language("en")
        yield
    finally:
        set_language(language)


@contextlib.contextmanager
def _dialog(settings=None, mode=DataTipMode.MAXIMUM):
    """A Snap dialog on ``settings`` (a fresh ``SnapSettings`` by default),
    in English, deleted afterwards."""
    import shiboken6
    from ogr_ui.dialogs.snap_dialog import SnapDialog
    _app()
    settings = SnapSettings() if settings is None else settings
    with _english():
        d = SnapDialog(settings, mode, None)
        try:
            yield settings, d
        finally:
            if shiboken6.isValid(d):
                shiboken6.delete(d)


@contextlib.contextmanager
def _swap(owner, name, value):
    raw = (owner.__dict__.get(name, _MISSING) if isinstance(owner, type)
           else getattr(owner, name))
    setattr(owner, name, value)
    try:
        yield
    finally:
        if raw is _MISSING:
            delattr(owner, name)
        else:
            setattr(owner, name, raw)


@contextlib.contextmanager
def _no_modals():
    from PySide6.QtWidgets import QDialog, QMessageBox

    def modal(*a, **k):
        raise AssertionError("a modal window")

    with contextlib.ExitStack() as stack:
        stack.enter_context(_swap(QDialog, "exec", modal))
        for name in ("information", "warning", "critical", "question"):
            stack.enter_context(_swap(QMessageBox, name,
                                      staticmethod(modal)))
        yield


@contextlib.contextmanager
def _spanish_with(theme):
    """Spanish and ``theme``, and everything put back afterwards."""
    from PySide6.QtCore import QLibraryInfo, QTranslator
    from PySide6.QtGui import QPalette
    from ogr_ui.i18n import current_language, set_language
    from ogr_ui.themes import apply_theme
    app = _app()
    sheet, palette = app.styleSheet(), QPalette(app.palette())
    language = current_language()
    # Qt's own Spanish catalog, for the standard buttons of the box:
    # "Restore Defaults" is twice as long in Spanish
    qt_es = QTranslator()
    loaded = qt_es.load("qtbase_es",
                        QLibraryInfo.path(QLibraryInfo.TranslationsPath))
    try:
        if loaded:
            app.installTranslator(qt_es)
        apply_theme(app, theme)
        set_language("es")
        yield app
    finally:
        set_language(language)
        if loaded:
            app.removeTranslator(qt_es)
        app.setStyleSheet(sheet)
        app.setPalette(palette)


def _cut(dialog):
    """The buttons showing less than their text."""
    from PySide6.QtWidgets import QPushButton
    return [(b.text(), b.width(), b.sizeHint().width())
            for b in dialog.findChildren(QPushButton)
            if b.isVisible() and b.text()
            and b.width() < b.sizeHint().width()]


def _squeezed(dialog):
    """What ``dialog`` shows cut or squashed besides its buttons, as
    ``(kind, text, has, needs)``: text that wraps is measured in height,
    text that does not in width; a box lower than its own minimum."""
    from PySide6.QtWidgets import (QAbstractSpinBox, QCheckBox, QComboBox,
                                   QLabel, QRadioButton)

    def text_cut(kind, w):
        if w.hasHeightForWidth():
            need = w.heightForWidth(w.width())
            if w.height() < need:
                out.append((kind + " lines", w.text()[:60], w.height(), need))
        elif w.width() < w.sizeHint().width():
            out.append((kind, w.text()[:60], w.width(), w.sizeHint().width()))

    out = []
    for w in dialog.findChildren(QLabel):
        if w.isVisible() and w.text():
            text_cut("label", w)
    for cls in (QCheckBox, QRadioButton):
        for w in dialog.findChildren(cls):
            if w.isVisible() and w.text():
                text_cut("check", w)
    for cls in (QAbstractSpinBox, QComboBox):
        for w in dialog.findChildren(cls):
            if (w.isVisible()
                    and w.height() < w.minimumSizeHint().height()):
                out.append(("box", type(w).__name__, w.height(),
                            w.minimumSizeHint().height()))
    return out


#: Each control, a value different from the default to set it to, and the
#: field of SnapSettings it must move.
_CONTROLS = (
    ("chk_snap", False, "snap"),
    ("chk_ortho", True, "ortho"),
    ("chk_osnap", True, "osnap"),
    ("sp_gh", 2.5, "grid_h"),
    ("sp_gv", 3.5, "grid_v"),
    ("sp_vertex", 20.0, "vertex_tolerance_px"),
    ("sp_line", 21.0, "line_tolerance_px"),
    ("sp_grid", 22.0, "grid_tolerance_px"),
    ("sp_ext", 23.0, "extension_tolerance_px"),
    ("sp_angle", 7.5, "ortho_snap_angle_deg"),
)


def _set(widget, value):
    if isinstance(value, bool):
        widget.setChecked(value)
    else:
        widget.setValue(value)


# ======================================================================
# Ported from Slip2D tests/test_m1_datatips_snap_v151.py, TestSnapDialog
# ======================================================================
class TestSnapDialog:
    def test_shows_the_current_settings(self):
        given = SnapSettings(snap=False, ortho=True, osnap=True, grid_h=2.0,
                             grid_v=4.0, vertex_tolerance_px=15.0,
                             line_tolerance_px=9.0, grid_tolerance_px=6.0,
                             extension_tolerance_px=11.0,
                             ortho_snap_angle_deg=3.0)
        with _dialog(given) as (s, d):
            for name, _value, attr in _CONTROLS:
                w = getattr(d, name)
                shown = (w.isChecked() if hasattr(w, "isChecked")
                         and w.isCheckable() else w.value())
                assert abs(float(shown) - float(getattr(s, attr))) < 1e-9, \
                    name

    def test_accept_writes_back_to_the_engine(self):
        with _dialog() as (s, d):
            d.sp_gh.setValue(2.5)
            d.sp_gv.setValue(3.5)
            d.chk_osnap.setChecked(True)
            d.sp_angle.setValue(7.5)
            d._accept()
            assert abs(s.grid_h - 2.5) < 1e-9
            assert abs(s.grid_v - 3.5) < 1e-9
            assert s.osnap is True
            assert abs(s.ortho_snap_angle_deg - 7.5) < 1e-9

    def test_accept_edits_the_object_in_place(self):
        """The engine and the status-bar words hold this very object: a
        copy handed back would leave them reading the old one."""
        with _dialog() as (s, d):
            d.sp_gh.setValue(2.5)
            d._accept()
            assert d.settings is s
            assert abs(s.grid_h - 2.5) < 1e-9

    def test_data_tip_mode_collected(self):
        with _dialog() as (_s, d):
            d.cbo_tips.setCurrentIndex(
                d.cbo_tips.findData(DataTipMode.MINIMUM))
            d._accept()
            assert d.data_tip_mode == DataTipMode.MINIMUM

    def test_all_three_modes_offered(self):
        with _dialog() as (_s, d):
            offered = {d.cbo_tips.itemData(i)
                       for i in range(d.cbo_tips.count())}
            assert offered == {DataTipMode.NONE, DataTipMode.MINIMUM,
                               DataTipMode.MAXIMUM}

    def test_tolerances_are_labelled_in_pixels(self):
        """They are pixels on purpose — converted by the canvas, which is
        what keeps snapping equally easy at any zoom. Labelling them
        stops anyone 'fixing' them into metres."""
        from PySide6.QtWidgets import QLabel
        with _dialog() as (_s, d):
            for w in (d.sp_vertex, d.sp_line, d.sp_grid, d.sp_ext):
                assert w.suffix().strip() == "px"
            text = " ".join(" ".join(la.text().split())
                            for la in d.findChildren(QLabel))
            assert "SCREEN PIXELS" in text

    def test_defaults_restore(self):
        with _dialog() as (_s, d):
            d.sp_gh.setValue(99.0)
            d._defaults()
            assert abs(d.sp_gh.value() - SnapSettings().grid_h) < 1e-9


# ======================================================================
# The dialog on its own (OGR GUI 0.1.0)
# ======================================================================
class TestEveryControlMovesTheSettings:
    """Rule 7: a control whose change does not reach the settings would be
    a setting that does nothing."""

    def test_each_control_moves_its_field(self):
        for name, value, attr in _CONTROLS:
            with _dialog() as (s, d):
                before = getattr(SnapSettings(), attr)
                assert getattr(s, attr) == before
                _set(getattr(d, name), value)
                d._accept()
                assert getattr(s, attr) != before, name
                assert abs(float(getattr(s, attr)) - float(value)) < 1e-9, \
                    name
                # and only its own field
                for _n, _v, other in _CONTROLS:
                    if other != attr:
                        assert getattr(s, other) == \
                            getattr(SnapSettings(), other), (name, other)

    def test_each_data_tip_choice_is_returned(self):
        for mode in DataTipMode:
            start = (DataTipMode.NONE if mode != DataTipMode.NONE
                     else DataTipMode.MAXIMUM)
            with _dialog(mode=start) as (_s, d):
                d.cbo_tips.setCurrentIndex(d.cbo_tips.findData(mode))
                d._accept()
                assert d.data_tip_mode == mode


class TestOkAndCancel:
    def test_nothing_is_written_before_ok(self):
        with _dialog() as (s, d):
            d.sp_gh.setValue(2.5)
            d.chk_ortho.setChecked(True)
            assert s.grid_h == SnapSettings().grid_h
            assert s.ortho is False

    def test_cancel_writes_nothing(self):
        with _dialog() as (s, d):
            for name, value, _attr in _CONTROLS:
                _set(getattr(d, name), value)
            d.cbo_tips.setCurrentIndex(d.cbo_tips.findData(DataTipMode.NONE))
            d.reject()
            assert s == SnapSettings()
            assert d.data_tip_mode == DataTipMode.MAXIMUM

    def test_ok_accepts_the_dialog(self):
        from PySide6.QtWidgets import QDialog
        with _dialog() as (_s, d):
            d._accept()
            assert d.result() == QDialog.Accepted


class TestRestoreDefaults:
    def test_every_control_goes_back(self):
        with _dialog() as (s, d):
            for name, value, _attr in _CONTROLS:
                _set(getattr(d, name), value)
            d.cbo_tips.setCurrentIndex(d.cbo_tips.findData(DataTipMode.NONE))
            d._defaults()
            d._accept()
            assert s == SnapSettings()
            assert d.data_tip_mode == DataTipMode.MAXIMUM

    def test_the_button_is_wired(self):
        from PySide6.QtWidgets import QDialogButtonBox
        with _dialog() as (_s, d):
            d.sp_line.setValue(50.0)
            box = d.findChildren(QDialogButtonBox)[0]
            box.button(QDialogButtonBox.RestoreDefaults).click()
            assert d.sp_line.value() == SnapSettings().line_tolerance_px

    def test_defaults_are_not_written_until_ok(self):
        given = SnapSettings(grid_h=4.0)
        with _dialog(given) as (s, d):
            d._defaults()
            assert s.grid_h == 4.0


class TestTheDataTipCombo:
    def test_opens_on_the_mode_given(self):
        for mode in DataTipMode:
            with _dialog(mode=mode) as (_s, d):
                assert d.cbo_tips.currentData() == mode
                assert d.data_tip_mode == mode

    def test_offered_in_order_of_how_much_it_says(self):
        with _dialog() as (_s, d):
            order = [d.cbo_tips.itemData(i)
                     for i in range(d.cbo_tips.count())]
            assert order == [DataTipMode.NONE, DataTipMode.MINIMUM,
                             DataTipMode.MAXIMUM]

    def test_labels_are_translated(self):
        from ogr_ui.dialogs.snap_dialog import SnapDialog
        from ogr_ui.i18n import current_language, set_language, tr
        import shiboken6
        _app()
        language = current_language()
        try:
            set_language("es")
            d = SnapDialog(SnapSettings(), DataTipMode.MINIMUM, None)
            try:
                assert d.cbo_tips.currentText() == tr("Minimum")
                assert d.cbo_tips.currentText() != "Minimum"
            finally:
                shiboken6.delete(d)
        finally:
            set_language(language)


# ======================================================================
# Ported from Slip2D tests/test_dialogs_fit_v1315.py (D293, D319-D321)
# ======================================================================
class TestItFitsInSpanish:
    def test_no_cut_and_within_the_screen(self):
        import shiboken6
        from ogr_ui.dialogs.snap_dialog import SnapDialog
        for theme in ("light", "dark"):
            with _spanish_with(theme) as app, _no_modals():
                d = SnapDialog(SnapSettings(), DataTipMode.MAXIMUM, None)
                try:
                    d.show()
                    app.processEvents()
                    assert _squeezed(d) == [], (theme, "opens",
                                                _squeezed(d))
                    ms = d.minimumSizeHint()
                    d.resize(ms)
                    app.processEvents()
                    assert _cut(d) == [], (theme, _cut(d))
                    assert _squeezed(d) == [], (theme, "minimum",
                                                _squeezed(d))
                    assert ms.width() <= _SCREEN[0], (theme, ms)
                    assert ms.height() <= _SCREEN[1], (theme, ms)
                finally:
                    d.hide()
                    shiboken6.delete(d)
