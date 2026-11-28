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
  the bit (RF-11).

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

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
