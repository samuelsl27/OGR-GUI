# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.4 — the numbers on screen, always with a decimal point
(spec 005).

OGR FEM2D asked (2026-11-28) for one way to write and read a number on
screen; the owner decided the point, in English and in Spanish, whatever
the machine's locale, and that a comma is not typed at all.

The invariants:

* **writing and reading, without Qt** (:mod:`ogr_ui.numbers`): a point and
  no thousands separator in both languages; one point read as the decimal
  mark (``1.000`` is 1), and a comma, a second point, spaces inside,
  ``nan`` and ``inf`` refused (RF-1, RF-4, RF-6, RF-8);
* **the number box** (:class:`ogr_ui.widgets.NumberBox`), typed with the
  keyboard under a Spanish and an English default locale of Qt: ``2.5``
  is 2.5 and shows with a point, a comma and a second point do not go in,
  typed or pasted, and what is out of range or half written goes back to
  the last value; Qt's default locale is left as it was (RF-5 to RF-10,
  RF-12). A plain ``QDoubleSpinBox`` under the Spanish locale reads
  ``2.5`` as 25: the finding of OGR FEM2D's T37, kept as evidence;
* **the pieces that write numbers** (the legend, the contour bands and the
  status bar) write with :func:`format_number` what 0.1.3 wrote,
  character for character, on a Spanish machine and in Spanish (RF-1,
  RF-2, RF-11);
* **the dialogs** of contours and of snap take a number box in each of
  their boxes, with the decimals, ranges, steps and suffixes of 0.1.3;
  what is typed with a point is what they return (RF-2, RF-5, RF-11);
* **the axes of the XY chart** with a point even with
  ``axes.formatter.use_locale`` on and a Spanish numeric locale in
  Python, and ``rcParams`` left as it was (RF-2, RF-3, RF-12).

Every test puts back the language, Qt's default locale, Python's numeric
locale and the clipboard (rule 5).

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import contextlib

from ogr_ui.numbers import format_number, read_number


@contextlib.contextmanager
def _language(code):
    from ogr_ui.i18n import current_language, set_language
    before = current_language()
    set_language(code)
    try:
        yield
    finally:
        set_language(before)


def _refused(text):
    try:
        got = read_number(text)
    except ValueError:
        return True
    raise AssertionError(f"{text!r} was read as {got!r}")


# ======================================================================
# Writing and reading, without Qt
# ======================================================================
class TestWritingANumber:
    def test_a_point_and_no_thousands_in_both_languages(self):
        for code in ("en", "es"):
            with _language(code):
                assert format_number(2.5, 3) == "2.500", code
                assert format_number(1000000.0, 2) == "1000000.00", code
                assert format_number(-0.125, 2) == "-0.12", code
                assert format_number(7.0, 0) == "7", code

    def test_scientific(self):
        for code in ("en", "es"):
            with _language(code):
                assert format_number(1250.0, 2, scientific=True) == "1.25e+03"
                assert format_number(0.0015, 3, scientific=True) == "1.500e-03"

    def test_signed(self):
        assert format_number(1.25, 3, signed=True) == "+1.250"
        assert format_number(-1.25, 3, signed=True) == "-1.250"
        assert format_number(0.0, 3, signed=True) == "+0.000"

    def test_what_the_pieces_wrote_in_013(self):
        # the f-strings of 0.1.3, written out: format_number gives the same
        for v, d in ((0.5, 3), (6.0, 3), (-0.0, 2), (123456.789, 4)):
            assert format_number(v, d) == f"{v:.{d}f}"
            assert format_number(v, d, scientific=True) == f"{v:.{d}e}"
            assert format_number(v, d, signed=True) == f"{v:+.{d}f}"

    def test_decimals_below_zero_are_none(self):
        assert format_number(2.5, -1) == "2"


class TestReadingANumber:
    def test_what_is_read(self):
        for text, value in (("2.5", 2.5), (".5", 0.5), ("5.", 5.0),
                            ("-0", 0.0), ("+3", 3.0), ("1.5e3", 1500.0),
                            ("1.5E-3", 0.0015), ("  2.5  ", 2.5),
                            ("7", 7.0)):
            assert read_number(text) == value, text

    def test_one_point_is_always_the_decimal_mark(self):
        assert read_number("1.000") == 1.0
        assert read_number("1.500") == 1.5

    def test_what_is_refused(self):
        for text in ("2,5", "1,000", "1.2.3", "1 000", "1_000", "abc",
                     "", " ", ".", "-", "1e", "e3", "nan", "inf",
                     "-infinity", "1e999", "1.234,56", "0x10"):
            assert _refused(text), text

    def test_the_same_in_both_languages(self):
        for code in ("en", "es"):
            with _language(code):
                assert read_number("2.5") == 2.5
                assert _refused("2,5")


class TestTheNumbersHaveNoQt:
    def test_it_imports_only_the_standard_library(self):
        import ast
        from pathlib import Path
        import ogr_ui.numbers as module
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                names.add((node.module or "").split(".")[0])
        assert names <= {"__future__", "math", "re"}, names


# ======================================================================
# The number box
# ======================================================================
def _app():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


#: The two machines a box has to work on: Spain's and England's.
_MACHINES = ("es_ES", "en_GB")


@contextlib.contextmanager
def _machine(name):
    """Qt's default locale set to ``name`` and put back (rule 5): what a
    box takes when it is made on a machine configured that way."""
    from PySide6.QtCore import QLocale
    _app()
    before = QLocale()
    QLocale.setDefault(QLocale(name))
    try:
        yield
    finally:
        QLocale.setDefault(before)


@contextlib.contextmanager
def _box(decimals=3, lo=-1e6, hi=1e6, value=0.0, **kw):
    from ogr_ui.widgets import NumberBox
    app = _app()
    box = NumberBox(**kw)
    box.setDecimals(decimals)
    box.setRange(lo, hi)
    box.setValue(value)
    try:
        yield box
    finally:
        box.deleteLater()
        app.processEvents()


def _type(box, text):
    """Typed with the keyboard over an emptied box, then Enter."""
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    box.clear()
    QTest.keyClicks(box, text)
    QTest.keyClick(box, Qt.Key_Return, Qt.NoModifier)


def _typed(box, text):
    """Typed with the keyboard over an emptied box, without leaving it:
    what the box let in."""
    from PySide6.QtTest import QTest
    box.clear()
    QTest.keyClicks(box, text)
    return box.cleanText()


@contextlib.contextmanager
def _clipboard(text):
    from PySide6.QtWidgets import QApplication
    cb = QApplication.clipboard()
    before = cb.text()
    cb.setText(text)
    try:
        yield
    finally:
        cb.setText(before)


class TestTheEvidence:
    def test_a_qt_box_on_a_spanish_machine_reads_a_point_as_nothing(self):
        from PySide6.QtWidgets import QDoubleSpinBox
        with _machine("es_ES"):
            box = QDoubleSpinBox()
            box.setDecimals(3)
            box.setRange(-1e6, 1e6)
            try:
                _type(box, "2.5")
                assert box.value() == 25.0      # what FEM2D's T37 saw
                box.setValue(2.5)
                assert box.text() == "2,500"
            finally:
                box.deleteLater()


class TestTheNumberBox:
    def test_a_point_is_read_and_shown(self):
        for machine in _MACHINES:
            with _machine(machine), _box() as box:
                _type(box, "2.5")
                assert box.value() == 2.5, machine
                assert box.text() == "2.500", machine

    def test_one_point_is_always_the_decimal_mark(self):
        for machine in _MACHINES:
            with _machine(machine), _box() as box:
                _type(box, "1.000")
                assert box.value() == 1.0, machine

    def test_a_comma_writes_nothing(self):
        for machine in _MACHINES:
            for code in ("en", "es"):
                with _machine(machine), _language(code), _box() as box:
                    assert _typed(box, "2,5") == "25", (machine, code)
                    assert _typed(box, "1,000") == "1000", (machine, code)
                    _type(box, "2,5")
                    assert box.value() == 25.0

    def test_a_second_point_and_a_letter_do_not_go_in(self):
        for machine in _MACHINES:
            with _machine(machine), _box() as box:
                assert _typed(box, "1.2.3") == "1.23", machine
                assert _typed(box, "1a2") == "12", machine
                assert _typed(box, "-1.5e3") == "-1.5e3", machine

    def test_a_paste_with_a_comma_changes_nothing(self):
        for machine in _MACHINES:
            for text in ("2,5", "1.234,56", "1,000.5"):
                with _machine(machine), _box(value=7.0) as box, \
                        _clipboard(text):
                    box.lineEdit().selectAll()
                    box.lineEdit().paste()
                    assert box.text() == "7.000", (machine, text)
                    assert box.value() == 7.0

    def test_a_paste_with_a_point_goes_in(self):
        with _machine("es_ES"), _box() as box, _clipboard("2.5"):
            box.lineEdit().selectAll()
            box.lineEdit().paste()
            box.interpretText()
            assert box.value() == 2.5

    def test_out_of_range_or_half_written_goes_back(self):
        for machine in _MACHINES:
            # the last valid value is the last one written: «1» of «1e»,
            # «5» of «50» (a Qt box keeps up with the keyboard)
            for text, last in (("-", 3.0), (".", 3.0), ("e3", 3.0),
                               ("1e", 1.0), ("50", 5.0)):
                with _machine(machine), _box(lo=0.0, hi=10.0,
                                             value=3.0) as box:
                    _type(box, text)
                    box.interpretText()
                    assert box.value() == last, (machine, text)
                    assert box.text() == format_number(last, 3)

    def test_with_a_suffix(self):
        with _machine("es_ES"), _box() as box:
            box.setSuffix(" m")
            _type(box, "2.5")
            assert box.value() == 2.5
            assert box.text() == "2.500 m"
            assert _typed(box, "2,5") == "25"

    def test_with_a_special_text_for_its_minimum(self):
        with _machine("es_ES"), _box(lo=0.0, hi=10.0, value=2.0) as box:
            box.setSpecialValueText("none")
            box.setValue(0.0)
            assert box.text() == "none"
            box.setValue(2.0)
            assert box.text() == "2.000"
            box.lineEdit().setText("none")
            box.interpretText()
            assert box.value() == 0.0

    def test_in_scientific_notation(self):
        with _machine("es_ES"), _box(value=1500.0, scientific=True) as box:
            assert box.text() == "1.500e+03"
            _type(box, "2.5e3")
            assert box.value() == 2500.0
            assert box.text() == "2.500e+03"

    def test_the_text_and_the_value_agree_when_rounded(self):
        for v in (0.12345, 0.12355, -2.00005, 1e5 + 0.00015):
            with _machine("es_ES"), _box(decimals=4, value=v) as box:
                assert box.text() == format_number(box.value(), 4), v
                assert read_number(box.text()) == box.value(), v

    def test_the_arrows_step_with_a_point(self):
        with _machine("es_ES"), _box(decimals=1, value=1.0) as box:
            box.setSingleStep(0.5)
            box.stepUp()
            assert box.value() == 1.5
            assert box.text() == "1.5"

    def test_it_is_a_qt_double_spin_box(self):
        from PySide6.QtWidgets import QDoubleSpinBox
        with _box() as box:
            assert isinstance(box, QDoubleSpinBox)

    def test_the_default_locale_is_left_as_it_was(self):
        from PySide6.QtCore import QLocale
        with _machine("es_ES"):
            with _box() as box:
                _type(box, "2.5")
            assert QLocale().name() == "es_ES"


# ======================================================================
# The pieces that write numbers
# ======================================================================
def _cases():
    for machine in _MACHINES:
        for code in ("en", "es"):
            yield machine, code


class TestWhatThePiecesWrite:
    """What 0.1.3 wrote, by hand: the same, character for character, on a
    Spanish machine and in Spanish too (RF-1, RF-2, RF-11)."""

    def test_the_continuous_legend(self):
        from ogr_ui.contours import ContourSettings
        from ogr_ui.widgets import ColourScaleLegend
        for machine, code in _cases():
            with _machine(machine), _language(code):
                legend = ColourScaleLegend()
                try:
                    fn = ContourSettings().colour_for
                    legend.configure(0.0, 1.0, fn, decimals=3)
                    assert legend.format_value(0.5) == "0.500"
                    assert legend.format_value(1234567.0) == "1234567.000"
                    assert legend.format_value(-0.0) == "-0.000"
                    legend.configure(0.0, 1.0, fn, decimals=2,
                                     scientific=True)
                    assert legend.format_value(1250.0) == "1.25e+03"
                finally:
                    legend.deleteLater()

    def test_the_bands_and_the_interval(self):
        from ogr_ui.contours import ContourSettings
        for machine, code in _cases():
            with _machine(machine), _language(code):
                s = ContourSettings(vmin=0.0, vmax=6.0, intervals=24)
                assert s.format_value(0.25) == "0.250"
                assert s.band_label(0) == "0.000"
                assert s.band_label(2) == "0.500"
                assert s.band_label(24) == "6.000+"
                s = ContourSettings(vmin=0.0, vmax=6000.0, intervals=4,
                                    decimals=1)
                assert s.band_label(4) == "6000.0+"
                s = ContourSettings(decimals=2, scientific=True)
                assert s.format_value(1250.0) == "1.25e+03"

    def test_the_status_bar(self):
        from PySide6.QtWidgets import QMainWindow
        from ogr_ui.widgets import OgrStatusBar
        for machine, code in _cases():
            with _machine(machine), _language(code):
                w = QMainWindow()
                try:
                    bar = OgrStatusBar(w)
                    bar.update_coords(1.25, -3.0)
                    assert bar.coord_label.text() == \
                        "X: +1.250   Y: -3.000"
                    bar.update_coords(12345.678, 0.0)
                    assert bar.coord_label.text() == \
                        "X: +12345.678   Y: +0.000"
                finally:
                    w.deleteLater()
                    _app().processEvents()

    def test_they_write_with_the_one_function(self):
        import ast
        from pathlib import Path
        import ogr_ui.contours as contours
        import ogr_ui.widgets.legend as legend
        import ogr_ui.widgets.status_bar as status_bar
        for module in (contours, legend, status_bar):
            tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
            names = {a.name for n in ast.walk(tree)
                     if isinstance(n, ast.ImportFrom)
                     and n.module == "ogr_ui.numbers" for a in n.names}
            assert "format_number" in names, module.__name__


# ======================================================================
# The dialogs, with the number box
# ======================================================================
def _write(box, text):
    """Typed with the keyboard over an emptied box, then read, as leaving
    the box does (Enter would also press the dialog's OK)."""
    from PySide6.QtTest import QTest
    box.clear()
    QTest.keyClicks(box, text)
    box.interpretText()


@contextlib.contextmanager
def _contour_dialog():
    import shiboken6
    from ogr_ui.contours import ContourField
    from ogr_ui.dialogs.contour_options_dialog import ContourOptionsDialog
    _app()
    field = ContourField("ratio", "Ratio")
    d = ContourOptionsDialog(field.defaults(), (field,), [1.0, 2.0], (),
                             None)
    try:
        yield d
    finally:
        if shiboken6.isValid(d):
            shiboken6.delete(d)


@contextlib.contextmanager
def _snap_dialog():
    import shiboken6
    from ogr_ui.canvas.snap_engine import SnapSettings
    from ogr_ui.dialogs.snap_dialog import SnapDialog
    _app()
    s = SnapSettings()
    d = SnapDialog(s)
    try:
        yield s, d
    finally:
        if shiboken6.isValid(d):
            shiboken6.delete(d)


#: The boxes of the snap dialog, a value to type into each, and the field
#: of SnapSettings it moves.
_SNAP_BOXES = (
    ("sp_gh", "2.5", 2.5, "grid_h"),
    ("sp_gv", "3.25", 3.25, "grid_v"),
    ("sp_vertex", "12.5", 12.5, "vertex_tolerance_px"),
    ("sp_line", "9.5", 9.5, "line_tolerance_px"),
    ("sp_grid", "6.5", 6.5, "grid_tolerance_px"),
    ("sp_ext", "11.5", 11.5, "extension_tolerance_px"),
    ("sp_angle", "7.5", 7.5, "ortho_snap_angle_deg"),
)


class TestTheDialogsTakeAPoint:
    """On a Spanish machine, in both languages: each box of the two dialogs
    shows a point, and what is typed with a point is what the dialog
    returns; a comma does not go in (RF-2, RF-5, RF-11)."""

    def test_the_contour_dialog(self):
        from ogr_ui.widgets import NumberBox
        for machine, code in _cases():
            with _machine(machine), _language(code), \
                    _contour_dialog() as d:
                d.chk_auto.setChecked(False)
                for box in (d.sp_min, d.sp_max):
                    assert isinstance(box, NumberBox)
                    assert "," not in box.text(), (machine, code)
                _write(d.sp_min, "0.5")
                _write(d.sp_max, "2.5")
                d.sp_int.setValue(4)
                got = d._collect()
                assert (got.vmin, got.vmax) == (0.5, 2.5), (machine, code)
                assert d.lbl_step.text() == "0.50", (machine, code)
                assert _typed(d.sp_max, "2,5") == "25"

    def test_the_snap_dialog(self):
        from ogr_ui.widgets import NumberBox
        for machine, code in _cases():
            with _machine(machine), _language(code), \
                    _snap_dialog() as (s, d):
                for name, text, value, _attr in _SNAP_BOXES:
                    box = getattr(d, name)
                    assert isinstance(box, NumberBox), name
                    assert "," not in box.text(), (machine, code, name)
                    _write(box, text)
                d._accept()
                for name, _text, value, attr in _SNAP_BOXES:
                    assert getattr(s, attr) == value, (machine, code, name)
                assert _typed(d.sp_gh, "2,5") == "25"

    def test_the_boxes_keep_what_they_had(self):
        # the same decimals, ranges, steps and suffixes as 0.1.3
        with _contour_dialog() as d:
            for box in (d.sp_min, d.sp_max):
                assert box.decimals() == 4
                assert (box.minimum(), box.maximum()) == (-1e9, 1e9)
        with _snap_dialog() as (_s, d):
            for name in ("sp_gh", "sp_gv"):
                box = getattr(d, name)
                # the dialog asks for a minimum of 1e-6, and Qt rounds it
                # to the box's 4 decimals: 0, as in 0.1.3 (reported with
                # spec 005, not changed by it)
                assert (box.decimals(), box.minimum(), box.maximum(),
                        box.singleStep()) == (4, 0.0, 1e6, 0.5), name
            for name in ("sp_vertex", "sp_line", "sp_grid", "sp_ext"):
                box = getattr(d, name)
                assert (box.decimals(), box.minimum(), box.maximum(),
                        box.suffix()) == (1, 1.0, 100.0, " px"), name
            assert (d.sp_angle.decimals(), d.sp_angle.minimum(),
                    d.sp_angle.maximum(), d.sp_angle.suffix()) == \
                (1, 0.0, 45.0, " °")


# ======================================================================
# The axes of the XY chart
# ======================================================================
@contextlib.contextmanager
def _chart_owner():
    """A main window to own the charts; every chart closed and freed."""
    from PySide6.QtWidgets import QMainWindow
    app = _app()
    w = QMainWindow()
    try:
        yield w
    finally:
        for dlg in list(getattr(w, "_chart_windows", [])):
            dlg.close()
            dlg.setParent(None)
            dlg.deleteLater()
        w.deleteLater()
        app.processEvents()


@contextlib.contextmanager
def _spanish_numbers():
    """Python's numeric locale set to a Spanish one where the machine has
    it, and put back (rule 5): what a program that asks matplotlib for
    the locale would write with. Yields whether one was found."""
    import locale
    before = locale.setlocale(locale.LC_NUMERIC)
    found = False
    for name in ("es_ES.UTF-8", "es_ES.utf8", "es_ES", "Spanish_Spain",
                 "Spanish"):
        try:
            locale.setlocale(locale.LC_NUMERIC, name)
        except locale.Error:
            continue
        found = locale.localeconv()["decimal_point"] == ","
        if found:
            break
    try:
        yield found
    finally:
        locale.setlocale(locale.LC_NUMERIC, before)


def _chart_axes(dlg):
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
    canvas = dlg.findChildren(FigureCanvasQTAgg)[0]
    canvas.draw()
    return canvas.figure.axes[0]


def _tick_texts(ax):
    return [t.get_text() for axis in (ax.xaxis, ax.yaxis)
            for t in axis.get_ticklabels() if t.get_text()]


class TestTheChartWritesAPoint:
    """The axes of the XY chart with a point even when a program asks
    matplotlib for the locale (RF-2, RF-3, RF-12)."""

    def test_with_the_locale_asked_for(self):
        import matplotlib
        from matplotlib.ticker import ScalarFormatter
        from ogr_ui.xy_chart import show_xy_chart
        with _chart_owner() as w, _spanish_numbers(), \
                matplotlib.rc_context({"axes.formatter.use_locale": True}):
            dlg = show_xy_chart(w, "t", [("", [0.0, 0.5, 1.5],
                                          [0.25, 1.75, 2.5])], "x", "y")
            ax = _chart_axes(dlg)
            for axis in (ax.xaxis, ax.yaxis):
                fmt = axis.get_major_formatter()
                assert isinstance(fmt, ScalarFormatter)
                assert fmt.get_useLocale() is False
            texts = _tick_texts(ax)
            assert texts, "no tick labels drawn"
            assert any("." in t for t in texts), texts
            assert not any("," in t for t in texts), texts

    def test_a_log_scale_is_still_drawn(self):
        import matplotlib
        from ogr_ui.xy_chart import show_xy_chart
        with _chart_owner() as w, \
                matplotlib.rc_context({"axes.formatter.use_locale": True}):
            dlg = show_xy_chart(w, "t", [("", [1, 2, 3], [1.0, 1e-5, 1e-10])],
                                "x", "y", yscale="log")
            ax = _chart_axes(dlg)
            assert ax.get_yscale() == "log"
            assert ax.xaxis.get_major_formatter().get_useLocale() is False

    def test_matplotlib_is_left_as_it_was(self):
        import matplotlib
        from ogr_ui.xy_chart import show_xy_chart
        with _chart_owner() as w:
            before = matplotlib.rcParams["axes.formatter.use_locale"]
            show_xy_chart(w, "t", [("", [0, 1], [0, 1])], "x", "y")
            assert matplotlib.rcParams["axes.formatter.use_locale"] == before
