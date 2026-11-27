# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.3 — the X,Y entry reads relative and polar points and the
decimal comma (spec 004).

OGR FEM2D asked for it (2026-11-25): the entry of the status bar took one
absolute point with decimal points only, so FEM2D took its validator off
and read the text itself. :mod:`ogr_ui.point_entry` reads what can be
typed, and the entry hands the program an absolute point.

The invariants:

* **the reader** (:func:`read_point`, no Qt): every absolute form, the
  decimal comma, a sign and an exponent; the relative and the polar from a
  reference point, as identities written by hand (rule 1); what is
  ambiguous or not a point refused with the message that says how to
  write it; and what 0.1.0 took gives the same point to the bit (RF-1 to
  RF-9, RF-16);
* **the entry** in a status bar of a test window: Enter hands over the
  point and empties the entry; a refusal hands nothing, keeps the text and
  says why in the bar, in English and in Spanish; the reference is given,
  changed and taken away; any character can be typed (RF-5, RF-7, RF-8,
  RF-10 to RF-12, RF-15, RF-16);
* **what is seen**: a general help, in both languages and naming no
  program's object, and the whole placeholder (RF-13, RF-14).

Every test puts back the language and deletes its window (rule 5).

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import contextlib

from ogr_ui.point_entry import PointEntryError, read_point

#: The three reasons, the keys of ``tr()``.
WRITE_A_POINT = ("Write a point as x, y (or x; y with decimal commas), "
                 "@dx, dy or @distance<angle.")
WRITE_A_POLAR = ("Write a polar point as @distance<angle, with the angle "
                 "in degrees.")
NEEDS_A_FIRST = "A relative point needs a first point: give it as x, y."

#: sqrt(3), written out: the sine of 60 degrees times 2.
_SQRT3 = 1.7320508075688772


def _refused(text, reference=None):
    try:
        got = read_point(text, reference)
    except PointEntryError as exc:
        return str(exc)
    raise AssertionError(f"{text!r} was read as {got!r}")


class TestAnAbsolutePoint:
    def test_every_separator(self):
        for text in ("1,5; 2,5", "1.5;2.5", "1,5;2,5", "1,5 2,5",
                     "1.5 2.5", "1.5, 2.5", "1,5, 2,5", "1.5,2.5",
                     "1.5   2.5", "1,5 ;  2,5"):
            assert read_point(text, None) == (1.5, 2.5), text

    def test_one_comma_with_no_space_separates(self):
        assert read_point("3,4", None) == (3.0, 4.0)
        assert read_point("1,5", None) == (1.0, 5.0)
        assert read_point("3,4 5", None) == (3.4, 5.0)

    def test_the_numbers(self):
        assert read_point("-1,5e3; +2", None) == (-1500.0, 2.0)
        assert read_point(".5 5.", None) == (0.5, 5.0)
        assert read_point(",5; 5,", None) == (0.5, 5.0)
        assert read_point("-0 1E-2", None) == (0.0, 0.01)

    def test_spaces_around(self):
        assert read_point("   1.5, 2.5  ", None) == (1.5, 2.5)

    def test_what_010_took_gives_the_same_point(self):
        for text, point in (("12.5, 3.2", (12.5, 3.2)),
                            ("12.5 3.2", (12.5, 3.2)),
                            ("12.5;3.2", (12.5, 3.2)),
                            ("-1.25, -2.5", (-1.25, -2.5)),
                            ("3, 4", (3.0, 4.0))):
            assert read_point(text, None) == point, text

    def test_the_reference_does_not_move_an_absolute_point(self):
        assert read_point("1; 2", (10.0, 10.0)) == (1.0, 2.0)


class TestARelativePoint:
    def test_by_a_shift(self):
        ref = (10.0, 5.0)
        assert read_point("@2, 0", ref) == (12.0, 5.0)
        assert read_point("@-1,5; 2,5", ref) == (8.5, 7.5)
        assert read_point("@ 1 2", ref) == (11.0, 7.0)
        assert read_point("  @0;0 ", ref) == ref

    def test_polar_identities(self):
        # cos 60 = 1/2, sin 60 = sqrt(3)/2
        x, y = read_point("@2<60", (1.0, 1.0))
        assert abs(x - 2.0) < 1e-15 and abs(y - (1.0 + _SQRT3)) < 1e-15
        # a sine or a cosine within 1e-15 of zero is zero: exact points
        assert read_point("@1<90", (3.0, 4.0)) == (3.0, 5.0)
        assert read_point("@1<180", (3.0, 4.0)) == (2.0, 4.0)
        assert read_point("@1<270", (3.0, 4.0)) == (3.0, 3.0)
        assert read_point("@1<0", (3.0, 4.0)) == (4.0, 4.0)
        assert read_point("@0<90", (3.0, 4.0)) == (3.0, 4.0)

    def test_polar_forms(self):
        assert read_point("@ 2,5 < 90", (0.0, 0.0)) == (0.0, 2.5)
        # a negative distance goes the other way; 405 degrees is 45
        x, y = read_point("@-1<45", (0.0, 0.0))
        assert abs(x + 0.5 ** 0.5) < 1e-15 and abs(y + 0.5 ** 0.5) < 1e-15
        x, y = read_point("@1<405", (0.0, 0.0))
        assert abs(x - 0.5 ** 0.5) < 1e-12 and abs(y - 0.5 ** 0.5) < 1e-12
        assert read_point("@3<-90", (0.0, 0.0)) == (0.0, -3.0)


class TestWhatIsRefused:
    def test_what_is_ambiguous_or_not_a_point(self):
        for text in ("1,5,2,5", "1,5,2.5", "1.5,2,5", "abc", "1", "1,5,",
                     "1 2 3", "1; 2; 3", "1;", "; 2", "1..5 2", "1,,5 2",
                     "x, y", "@", "@1", "@1, 2, 3", "1 2@"):
            assert _refused(text, (0.0, 0.0)) == WRITE_A_POINT, text

    def test_a_polar_point_written_wrong(self):
        for text in ("@1<", "@<2", "@1<2<3", "@a<2", "@1<2,5,1"):
            assert _refused(text, (0.0, 0.0)) == WRITE_A_POLAR, text

    def test_a_relative_point_with_no_reference(self):
        for text in ("@1, 2", "@1<90", "@ 0; 0"):
            assert _refused(text, None) == NEEDS_A_FIRST, text

    def test_what_is_not_finite(self):
        for text in ("nan 1", "inf; 2", "1e999 1", "1; -1e400"):
            assert _refused(text) == WRITE_A_POINT, text
        assert _refused("@1e999<0", (0.0, 0.0)) == WRITE_A_POLAR

    def test_nothing_written(self):
        for text in ("", "   "):
            assert _refused(text) == WRITE_A_POINT

    def test_a_reference_that_is_not_a_point(self):
        for bad in ((float("nan"), 0.0), (0.0, float("inf")), (1.0,),
                    "1, 2"):
            try:
                read_point("@1, 1", bad)
            except ValueError as exc:
                assert not isinstance(exc, PointEntryError), bad
            else:
                raise AssertionError(f"{bad!r} was taken")

    def test_the_reasons_have_their_spanish(self):
        from ogr_ui.i18n import package_translations
        es = package_translations("es")
        for key in (WRITE_A_POINT, WRITE_A_POLAR, NEEDS_A_FIRST):
            assert es.get(key) and es[key] != key, key


class TestTheReaderHasNoQt:
    def test_it_imports_only_the_standard_library(self):
        import ast
        from pathlib import Path
        import ogr_ui.point_entry as module
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names |= {a.name.split(".")[0] for a in node.names}
            elif isinstance(node, ast.ImportFrom):
                names.add((node.module or "").split(".")[0])
        assert names <= {"__future__", "math", "re", "typing"}, names


# ======================================================================
# The entry of the status bar
# ======================================================================
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
def _bar(width=None):
    """A test main window with an OgrStatusBar, and the points it hands
    over; shown at ``width`` when given."""
    from PySide6.QtWidgets import QMainWindow
    from ogr_ui.widgets.status_bar import OgrStatusBar
    app = _app()
    w = QMainWindow()
    bar = OgrStatusBar(w)
    w.setStatusBar(bar)
    points = []
    bar.manual_coords_submitted.connect(lambda x, y: points.append((x, y)))
    try:
        if width is not None:
            w.resize(width, 500)
            w.show()
            app.processEvents()
        yield bar, points
    finally:
        w.hide()
        w.deleteLater()
        app.processEvents()


def _type(field, text):
    """Typed with the keyboard, then Enter: what a person does."""
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    field.clear()
    QTest.keyClicks(field, text)
    QTest.keyClick(field, Qt.Key_Return, Qt.NoModifier)


class TestTheEntryHandsOverAnAbsolutePoint:
    def test_each_form_by_the_keyboard(self):
        with _bar() as (bar, points):
            bar.set_point_reference((10.0, 5.0))
            for text, point in (("1,5; 2,5", (1.5, 2.5)),
                                ("12.5, 3.2", (12.5, 3.2)),
                                ("@2, 0", (12.0, 5.0)),
                                ("@2<90", (10.0, 7.0)),
                                ("-1,5e1 2", (-15.0, 2.0))):
                _type(bar.coord_input, text)
                assert points[-1] == point, text
                assert bar.coord_input.text() == "", text
            assert len(points) == 5

    def test_the_old_signal_of_the_entry_too(self):
        with _bar() as (bar, points):
            own = []
            bar.coord_input.coords_submitted.connect(
                lambda x, y: own.append((x, y)))
            _type(bar.coord_input, "12.5;3.2")
            assert own == points == [(12.5, 3.2)]

    def test_an_empty_entry_does_nothing(self):
        with _bar() as (bar, points):
            bar.showMessage("Ready.")
            _type(bar.coord_input, "   ")
            assert points == []
            assert bar.currentMessage() == "Ready."

    def test_the_reference_given_changed_and_taken_away(self):
        with _bar() as (bar, points):
            bar.set_point_reference((1.0, 1.0))
            _type(bar.coord_input, "@1, 1")
            bar.set_point_reference((5.0, 5.0))
            _type(bar.coord_input, "@1, 1")
            bar.set_point_reference(None)
            _type(bar.coord_input, "@1, 1")
            assert points == [(2.0, 2.0), (6.0, 6.0)]
            assert bar.coord_input.text() == "@1, 1"

    def test_a_reference_that_is_not_a_point_is_refused_where_it_is_given(self):
        with _bar() as (bar, points):
            try:
                bar.set_point_reference((float("nan"), 0.0))
            except ValueError:
                pass
            else:
                raise AssertionError("a NaN reference was taken")

    def test_every_character_can_be_typed(self):
        from PySide6.QtTest import QTest
        with _bar() as (bar, points):
            QTest.keyClicks(bar.coord_input, "@1,5e2 < 9x;")
            assert bar.coord_input.text() == "@1,5e2 < 9x;"
            assert bar.coord_input.validator() is None


class TestARefusalSaysWhyAndKeepsTheText:
    def test_in_english_and_in_spanish(self):
        from ogr_ui.i18n import tr
        for language in ("en", "es"):
            with _language(language), _bar() as (bar, points):
                said = []
                bar.coord_input.point_refused.connect(said.append)
                for text, reason in (("1,5,2,5", WRITE_A_POINT),
                                     ("@1<", NEEDS_A_FIRST),
                                     ("abc", WRITE_A_POINT)):
                    _type(bar.coord_input, text)
                    assert bar.coord_input.text() == text, text
                    assert bar.currentMessage() == tr(reason), text
                    assert said[-1] == tr(reason)
                bar.set_point_reference((0.0, 0.0))
                _type(bar.coord_input, "@1<")
                assert bar.currentMessage() == tr(WRITE_A_POLAR)
                assert points == []
                if language == "es":
                    assert bar.currentMessage().startswith("Escribe")

    def test_the_reason_stays_until_the_next_message(self):
        with _bar() as (bar, points):
            _type(bar.coord_input, "abc")
            assert bar._until is None
            bar.showMessage("Next.")
            assert bar.currentMessage() == "Next."

    def test_twice_the_same(self):
        with _bar() as (bar, points):
            _type(bar.coord_input, "1 2 3")
            first = bar.currentMessage()
            from PySide6.QtCore import Qt
            from PySide6.QtTest import QTest
            QTest.keyClick(bar.coord_input, Qt.Key_Return, Qt.NoModifier)
            assert bar.currentMessage() == first
            assert bar.coord_input.text() == "1 2 3" and points == []


# ======================================================================
# What is seen
# ======================================================================
HELP = ("Type a point and press Enter: x, y (or x; y with decimal commas), "
        "@dx, dy from the last point, or @distance<angle in degrees.")
PLACEHOLDER = "x, y · @dx, dy · @d<a"


@contextlib.contextmanager
def _theme(name):
    from PySide6.QtGui import QPalette
    from ogr_ui.resources import icons
    from ogr_ui.themes import THEMES
    app = _app()
    sheet, palette = app.styleSheet(), QPalette(app.palette())
    try:
        app.setStyleSheet(THEMES[name])
        yield app
    finally:
        app.setStyleSheet(sheet)
        app.setPalette(palette)
        icons.reset_cache()


class TestWhatTheEntryShows:
    def test_a_general_help_in_both_languages(self):
        from ogr_ui.i18n import tr
        for language in ("en", "es"):
            with _language(language), _bar() as (bar, points):
                tip = bar.coord_input.toolTip()
                assert tip == tr(HELP), language
                for word in ("boundary", "polyline", "vertex", "contorno",
                             "polilínea", "vértice"):
                    assert word not in tip.lower(), (language, word)
        with _language("es"):
            assert tr(HELP) != HELP

    def test_a_program_gives_its_own(self):
        with _bar() as (bar, points):
            bar.coord_input.setToolTip("Mine.")
            assert bar.coord_input.toolTip() == "Mine."

    def test_the_whole_placeholder_in_both_themes(self):
        from PySide6.QtWidgets import QStyle, QStyleOptionFrame
        for theme in ("light", "dark"):
            with _theme(theme), _bar(1366) as (bar, points):
                field = bar.coord_input
                assert field.placeholderText() == PLACEHOLDER
                opt = QStyleOptionFrame()
                field.initStyleOption(opt)
                inner = field.style().subElementRect(
                    QStyle.SE_LineEditContents, opt, field)
                m = field.textMargins()
                room = inner.width() - m.left() - m.right() - 4
                need = field.fontMetrics().horizontalAdvance(PLACEHOLDER)
                assert need <= room, (theme, need, room, field.width())

    def test_the_messages_keep_their_room_at_1366(self):
        """The wider entry leaves the messages more than 200 px at 1366,
        as the test of 0.1.0 asks with no theme; with a theme it takes no
        more than its hint. Without fonts (offscreen, no QT_QPA_FONTDIR)
        every glyph is a wide box, so the themed room is not compared to
        a number of pixels: the entry is held to what it needs instead."""
        with _bar(1366) as (bar, points):
            assert bar.message_room() > 200, bar.message_room()
        for theme in ("light", "dark"):
            with _theme(theme), _bar(1366) as (bar, points):
                field = bar.coord_input
                assert field.width() == field.sizeHint().width(), theme
