# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
The status bar: its message is never hidden behind its indicators, its
indicators toggle and say so, and its X,Y field gives the exact point typed.

What this file protects, on ``ogr_ui.widgets.status_bar``:

* **ElidingStatusBar** (OGR Slip2D v0.1.328, D325; v0.1.418, D355): a long
  message ends in «…» where the indicators begin, its whole text is the
  bar's tooltip while it lasts, and ``currentMessage()`` answers the whole
  message; a short one is whole and has no tooltip; a wider bar shows more
  of it without restarting its time; clearing it, or its time running out,
  takes the tooltip away; a bar never shown keeps the whole message; a
  message Qt puts there by itself (an action's status tip) is cut the same
  way; a bare ``QStatusBar`` replaces one message with the next (v0.1.165);
* **OgrStatusBar** (v0.1.3; v0.1.51; v0.1.316, D301): SNAP and GRID start
  on, ORTHO and OSNAP off; a click or ``setChecked`` flips an indicator and
  the bar's own signal says so, once per change; the readout writes signed
  coordinates; ``add_toggle`` adds an indicator once (the same object the
  second time) and ``toggle`` finds it; ``retheme`` colours the readout, the
  separator and every indicator that is off, added ones too, by the active
  theme; an indicator that is on paints its own background in both themes;
* **the X,Y field**: ``12.5, 3.2``, ``12.5 3.2`` and ``12.5;3.2`` give the
  same point through ``coords_submitted`` and the bar's
  ``manual_coords_submitted``, to the bit, and the field is cleared; a
  letter is refused as it is typed, and one number alone gives nothing;
* the bar's texts go through ``tr()`` (rule 2): built in Spanish, the field
  and its tooltip read their Spanish.

From OGR Slip2D v0.1.486: ``tests/test_interpret_reasons_status_v1328.py``
(v0.1.328, D325: the long message), ``tests/test_texts_details_v1418.py``
(v0.1.418, D355: Qt's own messages), ``tests/test_m1_datatips_snap_v151.py``
(v0.1.51: ``add_toggle``/``toggle``), ``tests/test_annotation_clicks_v1416.py``
and ``tests/test_spanish_texts_v1432.py`` (the X,Y field, to the bit),
``tests/test_design_factor_report_gui_v1165.py`` (v0.1.165: a bare bar).
What those tests check of the main window (which indicator drives which
setting of the canvas, the DATA TIPS mode) stays in Slip2D.

The language, the sheet and the palette are put back (rule 5).
"""
from __future__ import annotations

import contextlib
import time

from PySide6.QtWidgets import QApplication, QStatusBar

#: The longest status message the third GUI test of Slip2D saw cut.
LONG = ("The Water Pressure Grid is read only with a grid groundwater method "
        "(Project Settings > Groundwater > Method), which also says what its "
        "values are.")


def _app():
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _language(code):
    from ogr_ui.i18n import current_language, set_language
    before = current_language()
    set_language(code)
    try:
        yield
    finally:
        set_language(before)


@contextlib.contextmanager
def _themed():
    from PySide6.QtGui import QPalette
    from ogr_ui.resources import icons
    app = _app()
    sheet, palette = app.styleSheet(), QPalette(app.palette())
    try:
        yield app
    finally:
        app.setStyleSheet(sheet)
        app.setPalette(palette)
        icons.reset_cache()


@contextlib.contextmanager
def _window(width=None, cls=None):
    """A main window with ``cls`` (OgrStatusBar) as its bar; shown at
    ``width`` when given, never shown otherwise."""
    from PySide6.QtWidgets import QMainWindow
    from ogr_ui.widgets.status_bar import OgrStatusBar
    app = _app()
    w = QMainWindow()
    bar = (cls or OgrStatusBar)(w)
    w.setStatusBar(bar)
    try:
        if width is not None:
            w.resize(width, 500)
            w.show()
            app.processEvents()
        yield w, bar
    finally:
        w.hide()
        w.deleteLater()
        app.processEvents()


def _shown(bar):
    """What the bar draws, not what ``currentMessage`` answers."""
    return QStatusBar.currentMessage(bar)


# ======================================================================
class TestALongMessageIsNotHidden:
    def test_it_ends_where_the_indicators_begin(self):
        with _window(1366) as (w, bar):
            bar.showMessage(LONG, 10000)
            shown = _shown(bar)
            assert bar.message_room() > 200, bar.message_room()
            assert bar.fontMetrics().horizontalAdvance(LONG) > \
                bar.message_room()
            assert shown.endswith("…"), shown
            assert bar.fontMetrics().horizontalAdvance(shown) <= \
                bar.message_room()
            # the whole text: in the tooltip, and for whoever asks
            assert bar.toolTip() == LONG
            assert bar.currentMessage() == LONG

    def test_the_room_ends_at_the_first_indicator(self):
        with _window(1366) as (w, bar):
            assert bar.message_room() == bar.snap.x() - bar.GAP_PX

    def test_control_a_short_one_is_whole(self):
        with _window(1366) as (w, bar):
            bar.showMessage("Ready.", 10000)
            assert _shown(bar) == "Ready."
            assert bar.toolTip() == ""
            assert bar.currentMessage() == "Ready."

    def test_a_wider_bar_shows_more_and_keeps_its_time(self):
        with _window(1366) as (w, bar):
            bar.showMessage(LONG, 10000)
            narrow = _shown(bar)
            until = bar._until
            w.resize(1900, 500)
            _app().processEvents()
            wide = _shown(bar)
            assert len(wide) > len(narrow), (narrow, wide)
            assert bar._until == until

    def test_its_tooltip_goes_with_it(self):
        with _window(1366) as (w, bar):
            bar.showMessage(LONG, 10000)
            assert bar.toolTip() == LONG
            bar.clearMessage()
            assert bar.toolTip() == "" and bar.currentMessage() == ""

    def test_and_when_its_time_runs_out(self):
        with _window(1366) as (w, bar):
            bar.showMessage(LONG, 50)
            assert bar.toolTip() == LONG
            deadline = time.monotonic() + 3.0
            while _shown(bar) and time.monotonic() < deadline:
                _app().processEvents()
                time.sleep(0.01)
            assert _shown(bar) == ""
            assert bar.toolTip() == "" and bar.currentMessage() == ""

    def test_a_bar_never_shown_keeps_the_whole_message(self):
        """The tests of a program read the message on windows that are
        never shown, where the bar has no width to cut it to."""
        with _window() as (w, bar):
            bar.showMessage(LONG, 10000)
            assert _shown(bar) == LONG
            assert bar.currentMessage() == LONG

    def test_a_status_tip_from_qt_is_cut_too(self):
        """D355: a message Qt shows by itself (an action's status tip under
        the pointer) never goes through ``showMessage``."""
        from PySide6.QtGui import QStatusTipEvent
        with _window(1366) as (w, bar):
            fm = bar.fontMetrics()
            assert fm.horizontalAdvance(LONG) > bar.message_room()
            QApplication.sendEvent(w, QStatusTipEvent(LONG))
            _app().processEvents()
            shown = _shown(bar)
            assert shown.endswith("…"), shown
            assert fm.horizontalAdvance(shown) <= bar.message_room()
            assert bar.toolTip() == LONG
            assert bar.currentMessage() == LONG
            QApplication.sendEvent(w, QStatusTipEvent(""))
            _app().processEvents()
            assert _shown(bar) == ""
            assert bar.toolTip() == ""

    def test_the_bare_eliding_bar_does_the_same(self):
        """``ElidingStatusBar`` alone, with an indicator of its own."""
        from PySide6.QtWidgets import QLabel
        from ogr_ui.widgets.status_bar import ElidingStatusBar
        with _window(600, cls=ElidingStatusBar) as (w, bar):
            bar.addPermanentWidget(QLabel("INDICADOR " * 4))
            _app().processEvents()
            bar.showMessage(LONG)
            assert _shown(bar).endswith("…")
            assert bar.currentMessage() == LONG

    def test_a_bare_status_bar_replaces_one_message_with_the_next(self):
        _app()
        bar = QStatusBar()
        try:
            bar.showMessage("first", 15000)
            assert bar.currentMessage() == "first"
            bar.showMessage("second", 10000)
            assert bar.currentMessage() == "second"
        finally:
            bar.deleteLater()


# ======================================================================
class TestTheIndicators:
    def test_they_start_as_they_always_did(self):
        with _window() as (w, bar):
            assert bar.snap.isChecked() and bar.grid.isChecked()
            assert not bar.ortho.isChecked() and not bar.osnap.isChecked()

    def test_each_one_says_its_change_once(self):
        with _window() as (w, bar):
            for name in ("snap", "grid", "ortho", "osnap"):
                seen = []
                getattr(bar, name + "_toggled").connect(seen.append)
                label = getattr(bar, name)
                was = label.isChecked()
                label.setChecked(not was)
                label.setChecked(not was)    # no change: no signal
                label.setChecked(was)
                assert seen == [not was, was], (name, seen)

    def test_a_click_flips_it(self):
        from PySide6.QtCore import Qt
        from PySide6.QtTest import QTest
        with _window(1366) as (w, bar):
            seen = []
            bar.ortho_toggled.connect(seen.append)
            QTest.mouseClick(bar.ortho, Qt.LeftButton)
            assert bar.ortho.isChecked() and seen == [True]
            QTest.mouseClick(bar.ortho, Qt.LeftButton)
            assert not bar.ortho.isChecked() and seen == [True, False]

    def test_the_readout_writes_signed_coordinates(self):
        with _window() as (w, bar):
            bar.update_coords(1.25, -3.0)
            assert bar.coord_label.text() == "X: +1.250   Y: -3.000"

    def test_add_toggle_adds_it_once(self):
        with _window(1366) as (w, bar):
            assert bar.toggle("DATA TIPS") is None
            a = bar.add_toggle("DATA TIPS", True)
            b = bar.add_toggle("DATA TIPS", False)
            assert a is b
            assert bar.toggle("DATA TIPS") is a
            assert a.isChecked()
            _app().processEvents()
            assert a.isVisible() and a.parent() is not None
            # it toggles as the others do
            seen = []
            a.toggled.connect(seen.append)
            a.setChecked(False)
            assert seen == [False]


class TestTheTheme:
    def test_retheme_follows_the_active_theme(self):
        from ogr_ui.themes import THEMES, theme_color
        with _themed() as app, _window() as (w, bar):
            extra = bar.add_toggle("DATA TIPS", False)
            for theme in ("light", "dark"):
                app.setStyleSheet(THEMES[theme])
                bar.retheme()
                assert theme_color("status_text", theme) in \
                    bar.coord_label.styleSheet()
                assert theme_color("separator", theme) in \
                    bar._sep.styleSheet()
                for off in (bar.ortho, bar.osnap, extra):
                    assert theme_color("toggle_off", theme) in \
                        off.styleSheet(), (theme, off.text())

    def test_an_indicator_that_is_on_paints_its_own_background(self):
        from ogr_ui.themes import THEMES
        with _themed() as app, _window() as (w, bar):
            sheets = {}
            for theme in ("light", "dark"):
                app.setStyleSheet(THEMES[theme])
                bar.retheme()
                sheets[theme] = bar.snap.styleSheet()
                assert "background: #b9d7f7" in sheets[theme], sheets[theme]
            assert sheets["light"] == sheets["dark"]


# ======================================================================
def _type(field, text):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    field.clear()
    QTest.keyClicks(field, text)
    QTest.keyClick(field, Qt.Key_Return, Qt.NoModifier)


class TestTheXYField:
    def test_every_separator_gives_the_same_point_to_the_bit(self):
        with _window(1366) as (w, bar):
            own, barwide = [], []
            bar.coord_input.coords_submitted.connect(
                lambda x, y: own.append((x, y)))
            bar.manual_coords_submitted.connect(
                lambda x, y: barwide.append((x, y)))
            for text in ("12.5, 3.2", "12.5 3.2", "12.5;3.2"):
                _type(bar.coord_input, text)
                assert bar.coord_input.text() == "", text
            assert own == [(12.5, 3.2)] * 3, own
            assert barwide == own
            _type(bar.coord_input, "-1.25, -2.5")
            assert own[-1] == (-1.25, -2.5)

    def test_a_letter_is_refused_and_one_number_gives_nothing(self):
        """0.1.3 (spec 004), on purpose: a letter can be typed now, and
        Enter refuses it, keeping the text and saying why (until 0.1.2 the
        validator kept it out and the field was left empty)."""
        with _window(1366) as (w, bar):
            seen = []
            bar.manual_coords_submitted.connect(
                lambda x, y: seen.append((x, y)))
            field = bar.coord_input
            _type(field, "x")
            assert seen == [] and field.text() == "x"
            assert bar.currentMessage() != ""
            field.setText("12.5")
            field._submit()
            field.setText("1, 2, 3")
            field._submit()
            assert seen == []

    def test_its_texts_are_translated(self):
        from ogr_ui.i18n import tr
        from ogr_ui.widgets.status_bar import _CoordInput
        _app()
        with _language("es"):
            # 0.1.3 (spec 004), on purpose: a general help, no longer
            # Slip2D's ("While drawing a boundary ... polyline", rule 10)
            key = ("Type a point and press Enter: x, y (or x; y with decimal "
                   "commas), @dx, dy from the last point, or @distance<angle "
                   "in degrees.")
            spanish = tr(key)
            assert spanish != key
            field = _CoordInput()
            try:
                assert field.toolTip() == spanish
            finally:
                field.deleteLater()
            with _window() as (w, bar):
                from PySide6.QtWidgets import QLabel
                texts = {lab.text() for lab in bar.findChildren(QLabel)}
                assert tr("Enter X,Y:") in texts
                assert tr("Enter X,Y:") != "Enter X,Y:"
