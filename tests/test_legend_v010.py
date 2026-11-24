# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.0 — the colour legend and the status-bar words
(``ogr_ui.widgets.legend``: ``ColourScaleLegend``, ``ToggleLabel``,
``StatusIndicators``), with no window around them.

The invariants:

* **the legend cannot disagree with the drawing**: it holds the very
  colour function it is given (a contour settings' ``colour_for``) and the
  bands and labels of those settings, the last one ending in ``+``; it
  survives a degenerate range and a colour function that fails, and it
  paints in every mode;
* **its title is the program's**: the default is empty (OGR Slip2D's was
  "Factor of safety", a text of that program) and a long one wraps at the
  legend's width instead of being cut;
* **the status words toggle by clicking them**, emit only on a real
  change, look different when on, and keep their English name as their
  key while the text shown is translated.

Ported from OGR Slip2D (v0.1.486):

* ``tests/test_interpret_i1_v149.py`` (v0.1.49, Interpret phase I1):
  ``TestColourScaleLegend`` and ``TestStatusIndicators``, on a legend and a
  ``QStatusBar`` of the test's own instead of the interpret window's. Left
  out: the range, the marker and the one-colour-function tests read the
  interpret window's results and contour settings (the marker and the
  shared function are tested here on values the test gives), and
  ``TestActiveAlgorithmAndLabel``, ``TestMethodSwitchKeepsEverythingInStep``
  and ``TestViewMenu`` are that window's.
* ``tests/test_slide_legend_v182.py`` (v0.1.82):
  ``test_the_legend_shows_the_same_bands`` and
  ``test_legend_paints_without_error``, on bands the test gives.
* ``tests/test_sixth_test_details_v1421.py`` (v0.1.421, D363): that the
  legend's title is not cut, here on the legend alone at its minimum width.

New here: that only the shown text of a status word is translated and its
key stays English, which ``ToggleLabel`` says of itself (v0.1.321, D300)
and no Slip2D test checked on the widget alone.
"""
from __future__ import annotations

import contextlib

from PySide6.QtWidgets import QApplication

from ogr_ui.contours import ContourMode, ContourSettings

_NAMES = {"DATA TIPS", "SNAP", "GRID", "ORTHO", "OSNAP"}


def _app():
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _language(code="en"):
    from ogr_ui.i18n import current_language, set_language
    before = current_language()
    try:
        set_language(code)
        yield
    finally:
        set_language(before)


@contextlib.contextmanager
def _legend():
    import shiboken6
    from ogr_ui.widgets.legend import ColourScaleLegend
    _app()
    with _language("en"):
        legend = ColourScaleLegend()
        try:
            yield legend
        finally:
            if shiboken6.isValid(legend):
                shiboken6.delete(legend)


@contextlib.contextmanager
def _indicators(initial=None, language="en"):
    import shiboken6
    from PySide6.QtWidgets import QStatusBar
    from ogr_ui.widgets.legend import StatusIndicators
    _app()
    with _language(language):
        bar = QStatusBar()
        try:
            yield StatusIndicators(bar, initial)
        finally:
            if shiboken6.isValid(bar):
                shiboken6.delete(bar)


def _paint(widget, w=120, h=300):
    from PySide6.QtGui import QPixmap
    widget.resize(w, h)
    pm = QPixmap(w, h)
    widget.render(pm)               # must not raise
    return pm


def _press(label, button=None):
    from PySide6.QtCore import QPoint, QPointF, Qt
    from PySide6.QtGui import QMouseEvent
    button = Qt.LeftButton if button is None else button
    ev = QMouseEvent(QMouseEvent.MouseButtonPress, QPointF(QPoint(3, 3)),
                     QPointF(QPoint(3, 3)), button, button, Qt.NoModifier)
    label.mousePressEvent(ev)


# ======================================================================
# Ported from Slip2D tests/test_interpret_i1_v149.py, TestColourScaleLegend
# ======================================================================
class TestColourScaleLegend:
    def test_the_default_title_is_empty(self):
        """The program says what the legend maps: a title of its own here
        would be one program's text in every program."""
        with _legend() as legend:
            assert legend._title == ""

    def test_range_is_what_was_configured(self):
        with _legend() as legend:
            s = ContourSettings(vmin=0.8, vmax=2.4)
            legend.configure(s.vmin, s.vmax, s.colour_for)
            assert legend.value_range() == (0.8, 2.4)

    def test_value_is_marked(self):
        with _legend() as legend:
            legend.configure(0.0, 3.0, ContourSettings().colour_for,
                             mark=1.234)
            assert abs(legend._mark - 1.234) < 1e-12
            legend.configure(0.0, 3.0, ContourSettings().colour_for)
            assert legend._mark is None

    def test_legend_and_canvas_use_one_colour_function(self):
        """The legend and the drawing must ask the same object for the
        colour of a value; otherwise they can disagree silently."""
        s = ContourSettings(vmin=0.0, vmax=6.0)
        with _legend() as legend:
            legend.configure(s.vmin, s.vmax, s.colour_for)
            assert legend._colour_fn == s.colour_for
            for value in (0.8, 1.2, 2.0, 5.0):
                assert legend._colour_fn(value) == s.colour_for(value)
            # a change of the settings reaches the legend with no plumbing
            s.palette = "Viridis"
            assert legend._colour_fn(1.2) == s.colour_for(1.2)

    def test_number_formatting(self):
        with _legend() as legend:
            fn = ContourSettings().colour_for
            legend.configure(0.0, 1.0, fn, decimals=3)
            assert legend.format_value(0.5) == "0.500"
            legend.configure(0.0, 1.0, fn, decimals=2, scientific=True)
            assert "e" in legend.format_value(0.5)

    def test_degenerate_range_is_handled(self):
        """A model where every value is the same must not make the legend
        divide by zero."""
        with _legend() as legend:
            legend.configure(1.5, 1.5, ContourSettings().colour_for)
            vmin, vmax = legend.value_range()
            assert vmax > vmin
            legend.configure(2.0, 1.0, ContourSettings().colour_for)
            vmin, vmax = legend.value_range()
            assert vmax > vmin
            _paint(legend)

    def test_paints_without_error(self):
        with _legend() as legend:
            legend.configure(0.0, 3.0, ContourSettings(
                mode=ContourMode.SMOOTH).colour_for, mark=1.2)
            _paint(legend)


class TestConfigure:
    def test_options_left_out_keep_their_value(self):
        with _legend() as legend:
            fn = ContourSettings().colour_for
            legend.configure(0.0, 1.0, fn, title="Head (m)", steps=6,
                             decimals=4, scientific=True)
            legend.configure(0.0, 2.0, fn)
            assert legend._title == "Head (m)"
            assert legend._steps == 6
            assert legend._decimals == 4 and legend._scientific is True

    def test_steps_and_decimals_are_clamped(self):
        with _legend() as legend:
            legend.configure(0.0, 1.0, None, steps=0, decimals=-3)
            assert legend._steps == 2
            assert legend._decimals == 0

    def test_bands_and_labels_are_only_for_this_call(self):
        """A banded configure followed by a smooth one must not leave the
        old swatches explaining a gradient they do not draw."""
        s = ContourSettings(vmin=0.0, vmax=6.0, intervals=24)
        with _legend() as legend:
            legend.configure(0.0, 6.0, s.colour_for, bands=s.band_colours(),
                             labels=[s.band_label(i) for i in range(25)])
            assert legend._bands is not None
            legend.configure(0.0, 6.0, s.colour_for)
            assert legend._bands is None and legend._labels is None


# ======================================================================
# Ported from Slip2D tests/test_slide_legend_v182.py
# ======================================================================
class TestTheBandedLegend:
    def _configure(self, legend, s):
        legend.configure(s.vmin, s.vmax, s.colour_for,
                         bands=s.band_colours(),
                         labels=[s.band_label(i)
                                 for i in range(s.intervals + 1)],
                         decimals=s.decimals)

    def test_the_legend_shows_the_same_bands(self):
        s = ContourSettings(vmin=0.0, vmax=6.0, intervals=24)
        with _legend() as legend:
            self._configure(legend, s)
            assert legend._bands == list(s.band_colours())
            assert len(legend._labels) == 25
            assert legend._labels[-1].endswith("+")
            assert legend._labels[0] == "0.000"

    def test_legend_paints_without_error(self):
        s = ContourSettings(vmin=0.0, vmax=6.0, intervals=24)
        with _legend() as legend:
            self._configure(legend, s)
            _paint(legend, 120, 400)
            _paint(legend, 96, 180)            # its minimum: labels thinned

    def test_the_bands_are_painted(self):
        """The bottom of the bar is the first band's colour, the top the
        last's."""
        from PySide6.QtGui import QColor
        s = ContourSettings(vmin=0.0, vmax=6.0, intervals=24)
        with _legend() as legend:
            self._configure(legend, s)
            img = _paint(legend, 120, 400).toImage()
            x = 12                              # inside the 20 px bar
            bottom = img.pixelColor(x, 400 - 8).name()
            assert bottom == QColor(s.band_colours()[0]).name()
            top = None
            for y in range(0, 400):
                c = img.pixelColor(x, y).name()
                if c == QColor(s.band_colours()[-1]).name():
                    top = y
                    break
            assert top is not None and top < 200, top

    def test_a_colour_function_that_fails_does_not_stop_the_paint(self):
        def broken(_v):
            raise ValueError("no colour")
        with _legend() as legend:
            legend.configure(0.0, 1.0, broken)
            _paint(legend)

    def test_no_colour_function_paints_only_the_title(self):
        with _legend() as legend:
            legend.configure(0.0, 1.0, None, title="Nothing yet")
            _paint(legend)


# ======================================================================
# Ported from Slip2D tests/test_sixth_test_details_v1421.py (D363)
# ======================================================================
class TestTheTitleIsNotCut:
    def test_a_long_title_wraps_at_the_width(self):
        from PySide6.QtGui import QFontMetrics
        with _legend() as legend:
            title = "Pore water pressure at the nodes (kPa)"
            legend.configure(0.0, 1.0, None, title=title)
            width = legend.minimumWidth()
            one_line = QFontMetrics(legend.title_font()).horizontalAdvance(
                title)
            assert one_line > width             # it would be cut on one line
            rect = legend.title_rect(width)
            assert rect.width() <= width
            line = QFontMetrics(legend.title_font()).height()
            assert rect.height() >= 2 * line

    def test_a_short_title_takes_one_line(self):
        from PySide6.QtGui import QFontMetrics
        with _legend() as legend:
            legend.configure(0.0, 1.0, None, title="FS")
            rect = legend.title_rect(legend.minimumWidth())
            assert rect.height() == QFontMetrics(legend.title_font()).height()

    def test_the_title_font_is_one_point_smaller(self):
        with _legend() as legend:
            base = legend.font().pointSizeF()
            assert abs(legend.title_font().pointSizeF()
                       - max(7.0, base - 1.0)) < 1e-9


# ======================================================================
# Ported from Slip2D tests/test_interpret_i1_v149.py, TestStatusIndicators
# ======================================================================
class TestStatusIndicators:
    def test_all_five_words_present(self):
        with _indicators() as ind:
            for name in _NAMES:
                assert name in ind.labels, name
            assert set(ind.labels) == _NAMES

    def test_clicking_toggles(self):
        """These must be toggleable by clicking the words, not only from a
        dialog."""
        with _indicators() as ind:
            lab = ind.labels["ORTHO"]
            before = lab.state()
            _press(lab)
            assert lab.state() is not before
            _press(lab)
            assert lab.state() is before

    def test_only_the_left_button_toggles(self):
        from PySide6.QtCore import Qt
        with _indicators() as ind:
            lab = ind.labels["GRID"]
            before = lab.state()
            _press(lab, Qt.RightButton)
            assert lab.state() is before

    def test_toggle_emits_a_signal(self):
        with _indicators() as ind:
            seen = []
            ind.connect("SNAP", lambda on: seen.append(on))
            ind.set_state("SNAP", True)
            assert seen == [True]
            _press(ind.labels["SNAP"])
            assert seen == [True, False]

    def test_setting_the_same_state_is_a_no_op(self):
        with _indicators() as ind:
            seen = []
            ind.connect("OSNAP", lambda on: seen.append(on))
            current = ind.state("OSNAP")
            ind.set_state("OSNAP", current)
            assert seen == []

    def test_visual_state_differs_when_on(self):
        """On and off must be legible at a glance."""
        with _indicators() as ind:
            lab = ind.labels["GRID"]
            lab.setState(False)
            off = lab.styleSheet()
            lab.setState(True)
            assert lab.styleSheet() != off
            assert "bold" in lab.styleSheet()

    def test_coordinates_readout(self):
        with _indicators() as ind:
            ind.set_coordinates(12.345, 67.891)
            text = ind.coords.text()
            assert "12.345" in text and "67.891" in text

    def test_states_snapshot(self):
        with _indicators() as ind:
            states = ind.states()
            assert set(states) == _NAMES
            assert all(isinstance(v, bool) for v in states.values())

    def test_initial_states(self):
        with _indicators({"SNAP": True, "GRID": True}) as ind:
            assert ind.states() == {"DATA TIPS": False, "SNAP": True,
                                    "GRID": True, "ORTHO": False,
                                    "OSNAP": False}

    def test_unknown_names_are_ignored(self):
        with _indicators() as ind:
            ind.set_state("NONSENSE", True)          # must not raise
            ind.connect("NONSENSE", lambda on: None)
            assert ind.state("NONSENSE") is False

    def test_the_words_are_in_the_status_bar(self):
        from PySide6.QtWidgets import QLabel
        with _indicators() as ind:
            inside = ind.status_bar.findChildren(QLabel)
            assert ind.coords in inside
            for lab in ind.labels.values():
                assert lab in inside


class TestTheKeyIsNotTranslated:
    def test_spanish_text_english_key(self):
        """D300: the name is also the key of the indicator; only the text
        shown is translated."""
        from ogr_ui.i18n import tr
        with _indicators(language="es") as ind:
            lab = ind.labels["DATA TIPS"]
            with _language("es"):
                want_text = tr("DATA TIPS")
                want_tip = tr("Click to toggle %s") % want_text
            assert want_text != "DATA TIPS"
            assert lab.text() == want_text
            assert lab.toolTip() == want_tip
            ind.set_state("DATA TIPS", True)
            assert ind.state("DATA TIPS") is True
            assert "DATA TIPS" in ind.states()
