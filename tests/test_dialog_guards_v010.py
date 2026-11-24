# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
The guards that keep a dialog usable: its size, the width of its buttons,
and the mouse wheel over its boxes.

What this file protects, on dialogs and widgets built here (the dialogs of
a program are that program's to test), with long Spanish texts of its own:

* ``ogr_ui.dialog_size`` (OGR Slip2D v0.1.315, D293; v0.1.326, D319–D321;
  v0.1.421, D363):
  - ``hold_wrapped_height`` keeps a window's minimum height at what its
    layout needs at its minimum width: without it (the control) a wrapped
    note gets one line and a number box is squashed; it keeps no Python
    reference to its window nor the window to it (the family of D310), and
    installing it twice adds nothing;
  - ``WrappingCheckBox`` wraps its text as a label does, gets its lines in a
    form layout, and keeps its text and a click on its last line;
  - ``open_at_content_size`` opens at what the content asks, never below
    what it is given nor beyond the screen; ``place_on_screen_of`` opens a
    window on its anchor's screen, never larger than it and whole inside;
  - ``list_width`` is the width a list needs to show its widest item;
    ``VerticalScrollArea`` is as wide as what it holds and scrolls up and
    down only (a plain ``QScrollArea`` is the control);
* ``ogr_ui.button_floor`` (D293): under a theme, a button of a button box is
  at least 100 px and never narrower than its text; the sheets set no
  ``min-width`` of their own (the old ``min-width: 70px`` cut Spanish
  buttons: the control); the floor is inert without a theme and leaves
  buttons outside a box alone;
* ``ogr_ui.wheel_guard`` (v0.1.285, D286): the wheel steps a number box or
  a drop-down only when it has the focus; boxes lose ``WheelFocus`` when
  polished; other widgets keep theirs; switched off, the wheel steps an
  unfocused box again (rule 7).

From OGR Slip2D v0.1.486: ``tests/test_dialogs_fit_v1315.py`` (v0.1.315,
D293; the floor, and its census's measure of a cut button),
``tests/test_dialogs_fit_more_v1326.py`` (v0.1.326, D319–D321; the
wrapping check box and the hold) and ``tests/test_wheel_guard_v1285.py``
(v0.1.285, D286). Their census of the program's dialogs, the hydraulic and
transient dialogs, and "the main window installs the guard" stay in Slip2D.

The sheet, the palette, the wheel guard and its switch are put back
(rule 5); no dialog is run with ``exec()``.
"""
from __future__ import annotations

import contextlib
import gc
import re

from PySide6.QtCore import QPoint, QPointF, QSize, Qt
from PySide6.QtWidgets import QApplication

#: Spanish that must not be cut: long, as the texts of the programs are.
NOTE = ("Los valores de esta página se aplican a todas las superficies de la "
        "búsqueda, y un valor fuera de su intervalo se recorta al límite más "
        "próximo antes de calcular, sin avisar otra vez de ello. ") * 3
CHECK = ("Anclajes: el factor de las acciones permanentes sobre la tensión "
         "efectiva de la adherencia del bulbo")
BUTTONS = ("Capturar condiciones actuales",
           "Restaurar los valores predeterminados", "Aceptar", "Cancelar")


def _app():
    return QApplication.instance() or QApplication([])


def _dispose(*widgets):
    app = _app()
    for w in widgets:
        if w is not None:
            w.hide()
            w.deleteLater()
    app.processEvents()


@contextlib.contextmanager
def _sheet(sheet=None, theme=None):
    """``theme`` applied, or ``sheet`` set, and the application's sheet and
    palette put back afterwards."""
    from PySide6.QtGui import QPalette
    from ogr_ui.resources import icons
    from ogr_ui.themes import apply_theme
    app = _app()
    old, palette = app.styleSheet(), QPalette(app.palette())
    try:
        if theme is not None:
            apply_theme(app, theme)
        if sheet is not None:
            app.setStyleSheet(sheet)
        yield app
    finally:
        app.setStyleSheet(old)
        app.setPalette(palette)
        icons.reset_cache()


def _note_and_box(hold, text=NOTE):
    from PySide6.QtWidgets import QDialog, QDoubleSpinBox, QLabel, QVBoxLayout
    from ogr_ui.dialog_size import hold_wrapped_height
    d = QDialog()
    lay = QVBoxLayout(d)
    note = QLabel(text)
    note.setWordWrap(True)
    lay.addWidget(note)
    box = QDoubleSpinBox()
    lay.addWidget(box)
    if hold:
        hold_wrapped_height(d)
    return d, note, box


def _at_its_minimum(d):
    app = _app()
    d.show()
    app.processEvents()
    d.resize(d.minimumSize())
    app.processEvents()


def _cut(dialog):
    """The buttons showing less than their text (Slip2D's census)."""
    from PySide6.QtWidgets import QPushButton
    return [(b.text(), b.width(), b.sizeHint().width())
            for b in dialog.findChildren(QPushButton)
            if b.isVisible() and b.text()
            and b.width() < b.sizeHint().width()]


def _box_dialog(texts=BUTTONS):
    from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
    d = QDialog()
    box = QDialogButtonBox()
    for t in texts:
        box.addButton(t, QDialogButtonBox.ActionRole)
    QVBoxLayout(d).addWidget(box)
    return d, box


# ======================================================================
class TestTheHold:
    def test_control_without_it_the_note_and_the_box_are_squashed(self):
        _app()
        d, note, box = _note_and_box(hold=False)
        try:
            _at_its_minimum(d)
            assert note.height() < note.heightForWidth(note.width())
            assert box.height() < box.minimumSizeHint().height()
        finally:
            _dispose(d)

    def test_with_it_both_are_whole_at_the_minimum(self):
        _app()
        d, note, box = _note_and_box(hold=True)
        try:
            _at_its_minimum(d)
            assert note.height() >= note.heightForWidth(note.width()), (
                note.height(), note.heightForWidth(note.width()))
            assert box.height() >= box.minimumSizeHint().height()
        finally:
            _dispose(d)

    def test_it_follows_the_content(self):
        """The hold runs on every new layout: a note shown later raises the
        minimum (a minimum set once would replace the layout's: D321)."""
        from PySide6.QtWidgets import QLabel
        app = _app()
        d, note, box = _note_and_box(hold=True)
        try:
            _at_its_minimum(d)
            before = d.minimumHeight()
            more = QLabel(NOTE)
            more.setWordWrap(True)
            d.layout().addWidget(more)
            app.processEvents()
            assert d.minimumHeight() > before, (before, d.minimumHeight())
        finally:
            _dispose(d)

    def test_neither_holds_the_other_in_python(self):
        from ogr_ui.dialog_size import _WrappedHeight, hold_wrapped_height
        _app()
        d, note, box = _note_and_box(hold=True)
        try:
            hold_wrapped_height(d)  # a second call adds nothing
            holds = d.findChildren(_WrappedHeight)
            assert len(holds) == 1
            assert not any(v is d for v in vars(holds[0]).values())
            assert not any(v is holds[0] for v in vars(d).values())
            gc.collect()
            _at_its_minimum(d)
            assert note.height() >= note.heightForWidth(note.width())
        finally:
            _dispose(d)


class TestTheWrappingCheckBox:
    def _box(self):
        from ogr_ui.dialog_size import WrappingCheckBox
        _app()
        return WrappingCheckBox(CHECK)

    def test_it_asks_for_more_lines_the_narrower_it_is(self):
        from PySide6.QtWidgets import QCheckBox
        box = self._box()
        plain = QCheckBox(CHECK)
        try:
            assert box.hasHeightForWidth()
            wide = box.heightForWidth(2000)
            narrow = box.heightForWidth(box.minimumSizeHint().width())
            assert narrow > wide, (narrow, wide)
            # its minimum is below one line of its text, the width a plain
            # check box imposes on its dialog
            assert box.minimumSizeHint().width() < \
                plain.minimumSizeHint().width()
        finally:
            _dispose(box, plain)

    def test_control_a_plain_check_box_does_not_wrap(self):
        from PySide6.QtWidgets import QCheckBox
        _app()
        plain = QCheckBox(CHECK)
        try:
            assert not plain.hasHeightForWidth()
            assert plain.minimumSizeHint().width() >= \
                plain.fontMetrics().horizontalAdvance(CHECK)
        finally:
            _dispose(plain)

    def test_a_form_layout_gives_it_its_lines(self):
        """A check box is Fixed in height, and a layout never gives a Fixed
        item more than its one-line hint: the first version wrapped its text
        and was cut to one line (20 px of 35)."""
        from PySide6.QtWidgets import QFormLayout, QSpinBox, QWidget
        box = self._box()
        page = QWidget()
        try:
            form = QFormLayout(page)
            form.addRow("Una etiqueta tan ancha como las de las opciones:",
                        QSpinBox())
            form.addRow("", box)
            page.resize(box.minimumSizeHint().width() * 2, 400)
            page.show()
            _app().processEvents()
            assert box.heightForWidth(box.width()) > \
                box.minimumSizeHint().height()
            assert box.height() >= box.heightForWidth(box.width()), (
                box.width(), box.height(), box.heightForWidth(box.width()))
        finally:
            _dispose(page)

    def test_it_keeps_its_text_and_a_click_on_the_last_line_ticks_it(self):
        from PySide6.QtTest import QTest
        box = self._box()
        try:
            width = box.minimumSizeHint().width()
            box.resize(width, box.heightForWidth(width))
            box.show()
            _app().processEvents()
            assert box.text() == CHECK
            assert not box.isChecked()
            QTest.mouseClick(box, Qt.LeftButton, Qt.NoModifier,
                             QPoint(box.width() - 4, box.height() - 4))
            assert box.isChecked()
        finally:
            _dispose(box)


class TestWhereADialogOpens:
    def test_at_its_content_never_below_what_it_is_given(self):
        from ogr_ui.dialog_size import open_at_content_size
        _app()
        # two buttons: the minimum of the four of BUTTONS is wider than the
        # offscreen screen (800 px), and the layout's minimum wins over it
        d, box = _box_dialog(BUTTONS[2:])
        try:
            open_at_content_size(d, QSize(200, 120))
            assert d.width() >= d.sizeHint().width()
            assert d.height() >= 120
            d.show()
            _app().processEvents()
            assert _cut(d) == [], _cut(d)
            d.hide()
            open_at_content_size(d, QSize(d.sizeHint().width() + 50, 300))
            assert d.width() == d.sizeHint().width() + 50
            assert d.height() == 300
        finally:
            _dispose(d)

    def test_never_beyond_the_screen(self):
        from ogr_ui.dialog_size import open_at_content_size
        _app()
        # one third of NOTE: at the 142 px of its minimum width the whole
        # of it needs more height than the offscreen screen has, and the
        # layout's minimum wins over the screen
        d, note, box = _note_and_box(hold=False, text=NOTE[:len(NOTE) // 3])
        try:
            open_at_content_size(d, QSize(100000, 100000))
            avail = d.screen().availableGeometry().size()
            assert d.width() <= avail.width() and \
                d.height() <= avail.height(), (d.size(), avail)
            # and it took all the screen gives: the bound, not the content
            assert d.size() == avail, (d.size(), avail)
        finally:
            _dispose(d)

    def test_it_holds_the_wrapped_height(self):
        """It installs the hold, so a dialog opened this way keeps its note
        whole however it is shrunk."""
        from ogr_ui.dialog_size import _WrappedHeight, open_at_content_size
        _app()
        d, note, box = _note_and_box(hold=False)
        try:
            open_at_content_size(d, QSize(300, 100))
            assert d.findChildren(_WrappedHeight)
            _at_its_minimum(d)
            assert note.height() >= note.heightForWidth(note.width())
        finally:
            _dispose(d)

    def test_on_its_anchors_screen_whole_and_no_larger(self):
        """D363: a window larger than the screen opened with its title bar
        above the top edge."""
        from PySide6.QtWidgets import QMainWindow, QWidget
        from ogr_ui.dialog_size import place_on_screen_of
        app = _app()
        anchor = QMainWindow()
        window = QWidget()
        try:
            anchor.resize(400, 300)
            anchor.show()
            app.processEvents()
            avail = anchor.screen().availableGeometry()
            place_on_screen_of(window, anchor,
                               QSize(avail.width() * 2, avail.height() * 2))
            assert window.screen() is anchor.screen()
            assert window.width() <= avail.width()
            assert window.height() <= avail.height()
            x, y = window.pos().x(), window.pos().y()
            assert x >= avail.left() and y >= avail.top(), (x, y)
            assert x + window.width() <= avail.right() + 1
            assert y + window.height() <= avail.bottom() + 1
            # one that fits keeps the size it asked for, centred on the
            # anchor
            place_on_screen_of(window, anchor, QSize(200, 100))
            assert window.size() == QSize(200, 100)
            centre = anchor.frameGeometry().center()
            assert abs(window.pos().x() + 100 - centre.x()) <= 4
        finally:
            _dispose(window, anchor)


class TestWideEnough:
    def test_list_width_shows_the_widest_item(self):
        from PySide6.QtWidgets import QListWidget
        from ogr_ui.dialog_size import list_width
        app = _app()
        lst = QListWidget()
        try:
            lst.addItems(["Agua", "Agua subterránea por elementos finitos",
                          "Transitorio"])
            lst.setFixedWidth(list_width(lst))
            lst.show()
            app.processEvents()
            assert lst.sizeHintForColumn(0) <= lst.viewport().width(), (
                lst.sizeHintForColumn(0), lst.viewport().width())
            with_bar = list_width(lst)
            lst.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            assert list_width(lst) == \
                with_bar - lst.verticalScrollBar().sizeHint().width()
        finally:
            _dispose(lst)

    def _area(self, cls):
        from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget
        area = cls()
        inner = QWidget()
        lay = QVBoxLayout(inner)
        for t in BUTTONS:
            lay.addWidget(QLabel(t * 2))
        area.setWidget(inner)
        area.setWidgetResizable(True)
        return area, inner

    def test_the_vertical_scroll_area_is_as_wide_as_its_content(self):
        from PySide6.QtWidgets import QScrollArea
        from ogr_ui.dialog_size import VerticalScrollArea
        app = _app()
        area, inner = self._area(VerticalScrollArea)
        plain, plain_inner = self._area(QScrollArea)
        try:
            need = inner.minimumSizeHint().width()
            assert area.minimumSizeHint().width() >= need
            # control: a plain one asks for almost nothing across
            assert plain.minimumSizeHint().width() < need
            area.resize(area.minimumSizeHint().width(), 80)
            area.show()
            app.processEvents()
            assert not area.horizontalScrollBar().isVisible()
        finally:
            _dispose(area, plain)


# ======================================================================
class TestTheButtonFloor:
    def test_a_box_button_is_never_narrower_than_its_text(self):
        with _sheet(theme="light") as app:
            d, box = _box_dialog()
            try:
                d.show()
                app.processEvents()
                d.resize(d.minimumSizeHint())
                app.processEvents()
                assert _cut(d) == [], _cut(d)
                for b in box.buttons():
                    assert b.minimumWidth() == max(100, b.sizeHint().width())
            finally:
                _dispose(d)

    def test_ok_and_cancel_keep_the_width_of_the_theme(self):
        from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
        with _sheet(theme="dark") as app:
            d = QDialog()
            QVBoxLayout(d).addWidget(QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel))
            try:
                d.show()
                app.processEvents()
                d.resize(d.minimumSizeHint())
                app.processEvents()
                for b in d.findChildren(QDialogButtonBox)[0].buttons():
                    # min-width 70 plus the 14 px padding on each side
                    assert b.width() >= 98, (b.text(), b.width())
            finally:
                _dispose(d)

    def test_the_sheets_set_no_minimum_of_their_own(self):
        """In a style sheet a minimum REPLACES the one the text asks for."""
        from ogr_ui.themes import THEMES
        for name, qss in THEMES.items():
            for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", qss):
                if "QPushButton" in sel:
                    assert "min-width" not in body, (name, sel)

    def test_control_the_old_rule_cut_them(self):
        """With ``min-width: 70px`` in the sheet (not a theme of ours, so
        the floor stays out of it) the Spanish buttons are cut."""
        from ogr_ui import button_floor
        from ogr_ui.themes import THEMES
        with _sheet(theme="light") as app:
            assert button_floor._floor is not None
            app.setStyleSheet(THEMES["light"]
                              + "\nQPushButton { min-width: 70px; }")
            d, box = _box_dialog()
            try:
                d.show()
                app.processEvents()
                d.resize(d.minimumSizeHint())
                app.processEvents()
                cut = [t for t, _has, _needs in _cut(d)]
                assert BUTTONS[0] in cut and BUTTONS[1] in cut, cut
            finally:
                _dispose(d)

    def test_it_is_inert_without_a_theme(self):
        """Installed by ``apply_theme`` and never removed: with the sheet
        put back, a box button gets no floor from it."""
        from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout
        from ogr_ui import button_floor
        with _sheet(sheet="") as app:
            button_floor.install(app)
            d = QDialog()
            QVBoxLayout(d).addWidget(QDialogButtonBox(QDialogButtonBox.Ok))
            try:
                d.show()
                app.processEvents()
                ok = d.findChildren(QDialogButtonBox)[0].buttons()[0]
                assert ok.minimumWidth() == 0
            finally:
                _dispose(d)

    def test_a_button_outside_a_box_has_no_floor(self):
        from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout
        with _sheet(theme="light") as app:
            d = QDialog()
            b = QPushButton("OK")
            QVBoxLayout(d).addWidget(b)
            try:
                d.show()
                app.processEvents()
                assert b.minimumWidth() == 0
            finally:
                _dispose(d)

    def test_install_is_idempotent(self):
        from ogr_ui import button_floor
        with _sheet(theme="light") as app:
            first = button_floor.install(app)
            assert button_floor.install(app) is first


# ======================================================================
def _wheel(widget, notches=3):
    from PySide6.QtGui import QWheelEvent
    app = _app()
    for _ in range(notches):
        ev = QWheelEvent(QPointF(5, 5),
                         QPointF(widget.mapToGlobal(QPoint(5, 5))),
                         QPoint(0, 0), QPoint(0, -120), Qt.NoButton,
                         Qt.NoModifier, Qt.NoScrollPhase, False)
        QApplication.sendEvent(widget, ev)
        app.processEvents()


class _Guarded:
    """The guard installed for the test, and the application as found."""

    def __enter__(self):
        from ogr_ui import wheel_guard
        self.was = wheel_guard.installed()
        self.switch = wheel_guard.WHEEL_NEEDS_FOCUS
        wheel_guard.install(_app())
        return self

    def __exit__(self, *exc):
        from ogr_ui import wheel_guard
        wheel_guard.WHEEL_NEEDS_FOCUS = self.switch
        if not self.was:
            wheel_guard.uninstall(_app())
        return False


def _form():
    """A dialog with two number boxes, a drop-down and a list, shown and
    active; built after the guard, so polished under it."""
    from PySide6.QtWidgets import (QComboBox, QDialog, QDoubleSpinBox,
                                   QListWidget, QVBoxLayout)
    app = _app()
    d = QDialog()
    lay = QVBoxLayout(d)
    d.first, d.second = QDoubleSpinBox(), QDoubleSpinBox()
    for box in (d.first, d.second):
        box.setDecimals(3)
        box.setSingleStep(0.001)
        box.setValue(0.01)
        lay.addWidget(box)
    d.combo = QComboBox()
    d.combo.addItems(["Gardner", "Van Genuchten", "Fredlund y Xing"])
    d.combo.setCurrentIndex(1)
    lay.addWidget(d.combo)
    d.listing = QListWidget()
    d.listing.setFocusPolicy(Qt.WheelFocus)
    lay.addWidget(d.listing)
    d.show()
    d.activateWindow()
    app.processEvents()
    return d


class TestTheWheel:
    def test_an_unfocused_box_does_not_change(self):
        with _Guarded():
            d = _form()
            try:
                d.first.setFocus()
                _app().processEvents()
                assert not d.second.hasFocus()
                before = d.second.value()
                _wheel(d.second)
                assert d.second.value() == before
            finally:
                _dispose(d)

    def test_an_unfocused_drop_down_does_not_change(self):
        with _Guarded():
            d = _form()
            try:
                d.first.setFocus()
                _app().processEvents()
                before = d.combo.currentIndex()
                _wheel(d.combo, 1)
                assert d.combo.currentIndex() == before
            finally:
                _dispose(d)

    def test_a_focused_box_still_changes(self):
        with _Guarded():
            d = _form()
            try:
                d.second.setFocus()
                _app().processEvents()
                assert d.second.hasFocus()
                before = d.second.value()
                _wheel(d.second)
                assert d.second.value() < before
            finally:
                _dispose(d)

    def test_boxes_lose_wheel_focus_and_nothing_else_does(self):
        with _Guarded():
            d = _form()
            try:
                for w in (d.first, d.second, d.combo):
                    assert w.focusPolicy() == Qt.FocusPolicy.StrongFocus, w
                assert d.listing.focusPolicy() == Qt.FocusPolicy.WheelFocus
            finally:
                _dispose(d)

    def test_switched_off_the_wheel_steps_an_unfocused_box(self):
        from ogr_ui import wheel_guard
        with _Guarded():
            wheel_guard.WHEEL_NEEDS_FOCUS = False
            d = _form()
            try:
                d.first.setFocus()
                _app().processEvents()
                before = d.second.value()
                _wheel(d.second)
                assert d.second.value() < before
            finally:
                _dispose(d)

    def test_install_is_idempotent_and_uninstall_removes_it(self):
        from ogr_ui import wheel_guard
        with _Guarded():
            first = wheel_guard.install(_app())
            assert wheel_guard.install(_app()) is first
            assert wheel_guard.installed()
            wheel_guard.uninstall(_app())
            assert not wheel_guard.installed()
            d = _form()
            try:
                d.first.setFocus()
                _app().processEvents()
                before = d.second.value()
                _wheel(d.second)
                # nothing guards it: Qt's own behaviour comes back
                assert d.second.value() < before
            finally:
                _dispose(d)
                # back as _Guarded expects it; it removes it on leaving if
                # it was not there before the test
                wheel_guard.install(_app())
