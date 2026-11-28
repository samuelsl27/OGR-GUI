# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.2.0 — in the X,Y entry, the comma separates the coordinates and
the point is the decimal mark (spec 006).

The owner's criterion of 2026-11-28, as in OGR FEM2D's D12 as she
modified it: a point is written ``x.x,x.x``. Only a comma separates the two
coordinates; the decimal comma, a lone space and a semicolon are no
longer read. An incompatible change: 0.2.0.

The invariants, of the reader (:func:`ogr_ui.point_entry.read_point`):

* one comma between two numbers, with or without spaces around it, each
  number with a decimal point, a sign and an exponent; the relative
  ``@dx,dy`` and the polar ``@d<a`` by the same reading of a number
  (RF-1 to RF-4);
* a lone space or a semicolon as the separator, a decimal comma, and more
  or fewer than one comma refused, with the reason that says how to write a
  point (RF-5 to RF-7); what was refused before still is (RF-8);
* what 0.1.4 took with decimal points and a comma gives the same point to
  the bit (RF-11);

and of what is seen, with the entry in a status bar of a test window: a
point with a comma is handed over, a decimal comma stays with the new
reason, in English and in Spanish; neither the reason nor the help speaks
of a decimal comma, and the placeholder is the same (RF-5, RF-6, RF-9 to
RF-11). Every test puts back the language and deletes its window (rule 5).

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import contextlib

from ogr_ui.point_entry import (NEEDS_A_FIRST, WRITE_A_POINT, WRITE_A_POLAR,
                                PointEntryError, read_point)


def _refused(text, reference=(0.0, 0.0)):
    try:
        got = read_point(text, reference)
    except PointEntryError as exc:
        return str(exc)
    raise AssertionError(f"{text!r} was read as {got!r}")


class TestWhatIsRead:
    def test_one_comma_with_or_without_spaces(self):
        for text in ("1.5,2.5", "1.5, 2.5", "1.5 ,2.5", "1.5 , 2.5",
                     "  1.5,2.5  ", "1.5,   2.5"):
            assert read_point(text, None) == (1.5, 2.5), text

    def test_the_numbers(self):
        assert read_point("-1.5e3,+2", None) == (-1500.0, 2.0)
        assert read_point(".5,5.", None) == (0.5, 5.0)
        assert read_point("-0, 1E-2", None) == (0.0, 0.01)
        assert read_point("3,4", None) == (3.0, 4.0)
        assert read_point("1,5", None) == (1.0, 5.0)    # a comma separates

    def test_a_relative_point(self):
        ref = (10.0, 5.0)
        assert read_point("@2,0", ref) == (12.0, 5.0)
        assert read_point("@-1.5, 2.5", ref) == (8.5, 7.5)
        assert read_point("@ 1.5 , 2", (1.0, 1.0)) == (2.5, 3.0)

    def test_a_polar_point(self):
        assert read_point("@2.5<90", (0.0, 0.0)) == (0.0, 2.5)
        assert read_point("@ 1.5 < 0", (1.0, 1.0)) == (2.5, 1.0)
        assert read_point("@1<90", (3.0, 4.0)) == (3.0, 5.0)


class TestWhatIsRefused:
    def test_a_lone_space_or_a_semicolon(self):
        for text in ("1.5 2.5", "1.5;2.5", "1.5; 2.5", "1 2", "1;2",
                     "12.5 3.2", "12.5;3.2"):
            assert _refused(text) == WRITE_A_POINT, text
        for text in ("@1 2", "@1;2"):
            assert _refused(text) == WRITE_A_POINT, text

    def test_a_decimal_comma(self):
        for text in ("1,5; 2,5", "1,5 2,5", "1,5,2,5", "1,5, 2,5",
                     "1,5,2.5", "1.5,2,5", ",5,5"):
            assert _refused(text) == WRITE_A_POINT, text
        assert _refused("@1,5<30") == WRITE_A_POLAR
        assert _refused("@1<2,5") == WRITE_A_POLAR

    def test_more_or_fewer_than_one_comma(self):
        for text in ("1.5", "1.5,2.5,3.5", "1.5,,2.5", ",2.5", "1.5,",
                     ",", "@1.5", "@1,2,3"):
            assert _refused(text) == WRITE_A_POINT, text

    def test_what_was_refused_still_is(self):
        for text in ("abc", "x, y", "", "   ", "@", "1..5,2", "nan,1",
                     "inf,2", "1e999,1", "1,-1e400", "1 2@"):
            assert _refused(text) == WRITE_A_POINT, text
        for text in ("@1<", "@<2", "@1<2<3", "@a<2", "@1e999<0"):
            assert _refused(text) == WRITE_A_POLAR, text
        for text in ("@1,2", "@1<90"):
            assert _refused(text, None) == NEEDS_A_FIRST, text


class TestWhat014TookWithAPoint:
    def test_the_same_point_to_the_bit(self):
        ref = (10.0, 5.0)
        for text, point in (("12.5, 3.2", (12.5, 3.2)),
                            ("12.5,3.2", (12.5, 3.2)),
                            ("-1.25, -2.5", (-1.25, -2.5)),
                            ("3, 4", (3.0, 4.0)),
                            ("@2, 0", (12.0, 5.0))):
            assert read_point(text, ref) == point, text
        x, y = read_point("@2<60", (1.0, 1.0))
        assert abs(x - 2.0) < 1e-15 and abs(y - (1.0 + 3 ** 0.5)) < 1e-15


class TestTheReaderReadsNumbersAsTheBoxesDo:
    def test_it_reads_with_read_number_and_has_no_qt(self):
        import ast
        from pathlib import Path
        import ogr_ui.point_entry as module
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names |= {a.name for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        assert names <= {"__future__", "math", "re", "typing",
                         "ogr_ui.numbers"}, names
        assert "ogr_ui.numbers" in names


# ======================================================================
# What is seen, and the entry in a status bar
# ======================================================================

#: The two texts of 0.2.0, written out: the reason and the help.
NEW_REASON = ("Write a point as x, y with a decimal point (1.5, 2.5), "
              "@dx, dy or @distance<angle.")
NEW_HELP = ("Type a point and press Enter: x, y with a decimal point, "
            "@dx, dy from the last point, or @distance<angle in degrees.")
#: The two of 0.1.3, which spoke of the decimal comma.
OLD_REASON = ("Write a point as x, y (or x; y with decimal commas), "
              "@dx, dy or @distance<angle.")
OLD_HELP = ("Type a point and press Enter: x, y (or x; y with decimal "
            "commas), @dx, dy from the last point, or @distance<angle in "
            "degrees.")


def _app():
    from PySide6.QtWidgets import QApplication
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
def _bar():
    from PySide6.QtWidgets import QMainWindow
    from ogr_ui.widgets.status_bar import OgrStatusBar
    app = _app()
    w = QMainWindow()
    bar = OgrStatusBar(w)
    w.setStatusBar(bar)
    points = []
    bar.manual_coords_submitted.connect(lambda x, y: points.append((x, y)))
    try:
        yield bar, points
    finally:
        w.deleteLater()
        app.processEvents()


def _type(field, text):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    field.clear()
    QTest.keyClicks(field, text)
    QTest.keyClick(field, Qt.Key_Return, Qt.NoModifier)


class TestTheEntryInTheBar:
    def test_a_point_with_a_comma_is_handed_over(self):
        with _bar() as (bar, points):
            for text in ("1.5,2.5", "1.5, 2.5", " 1.5 , 2.5 "):
                _type(bar.coord_input, text)
                assert bar.coord_input.text() == "", text
            assert points == [(1.5, 2.5)] * 3

    def test_a_decimal_comma_stays_with_its_reason(self):
        from ogr_ui.i18n import tr
        for code in ("en", "es"):
            with _language(code), _bar() as (bar, points):
                for text in ("1,5; 2,5", "1.5 2.5", "1.5;2.5"):
                    _type(bar.coord_input, text)
                    assert bar.coord_input.text() == text, (code, text)
                    assert bar.currentMessage() == tr(NEW_REASON), code
                assert points == []


class TestWhatIsSaid:
    def test_the_reason_and_the_help(self):
        assert WRITE_A_POINT == NEW_REASON
        with _bar() as (bar, _points):
            assert bar.coord_input.toolTip() == NEW_HELP

    def test_their_spanish(self):
        from ogr_ui.i18n import package_translations
        es = package_translations("es")
        assert es[NEW_REASON] == ("Escribe un punto como x, y con punto "
                                  "decimal (1.5, 2.5), @dx, dy o "
                                  "@distancia<ángulo.")
        assert es[NEW_HELP] == ("Escribe un punto y pulsa Intro: x, y con "
                                "punto decimal, @dx, dy desde el último "
                                "punto, o @distancia<ángulo en grados.")
        assert OLD_REASON not in es and OLD_HELP not in es

    def test_no_word_of_a_decimal_comma(self):
        from ogr_ui.i18n import tr
        for code in ("en", "es"):
            with _language(code), _bar() as (bar, _points):
                for text in (tr(WRITE_A_POINT), bar.coord_input.toolTip()):
                    low = text.lower()
                    assert "decimal comma" not in low, text
                    assert "coma decimal" not in low, text
                    assert "x; y" not in low, text

    def test_the_placeholder_is_the_same(self):
        with _bar() as (bar, _points):
            assert bar.coord_input.placeholderText() == \
                "x, y · @dx, dy · @d<a"
