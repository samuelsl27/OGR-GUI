# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
The two themes and the icons follow one another, and the light theme is the
application as it was before any theme.

What this file protects, on ``ogr_ui.themes`` and ``ogr_ui.resources.icons``:

* **the roles** (OGR Slip2D v0.1.316, D301): the light value of every role IS
  the literal the widgets wrote before roles existed, both themes have the
  same roles, and every text role reads at 4.0:1 or more on the window and
  on the status bar of its theme (the light theme's minimum before D301);
* **the active theme is read from the sheet** (D301): a test that puts the
  sheet back leaves no "dark" behind, and ``theme_color`` follows;
* **apply_theme** sets the sheet, a dark palette whose texts read, and for
  the light theme the palette the application had before any theme; it
  installs the button floor (D293) and forgets the icons built so far. It
  does NOT put back the sheet the application had before: the light theme
  is a sheet of its own, so whoever applies a theme restores the sheet;
* **a disabled entry looks disabled** in both themes (v0.1.288, D289),
  rendered, and every coloured selector of a sheet has its ``:disabled``
  colour; the disabled header of the dark theme reads (v0.1.326, D319);
* **the icons** (D301): an icon with no colour of its own reads on the dark
  menu, a dark grey one is lifted, a dark saturated one keeps its hue but
  lighter (``_for_theme``); a change of theme builds them again
  (``reset_cache``); Stretch Support has its own icon (v0.1.418, D355);
* **a program's own keys** (OGR GUI 0.1.0): ``register`` adds them, refuses a
  key the suite already has (and then adds none of the call), and forgets
  the icons built; ``unregister`` takes them away.

From OGR Slip2D v0.1.486: ``tests/test_dark_theme_v1316.py`` (v0.1.316,
D301; the parts on the themes and the icons, without the main window),
``tests/test_disabled_menus_v1288.py`` (v0.1.288, D289; its two rendered
tests and its census of the sheets), ``tests/test_dialogs_fit_more_v1326.py``
(v0.1.326, D319; the disabled header), ``tests/test_texts_details_v1418.py``
(v0.1.418, D355; Stretch Support's icon) and
``tests/test_surfaces_menu_labels_v1166.py`` (v0.1.166; ``has``).
``tests/test_annotation_dark_v1413.py`` (v0.1.413, D350) checks the canvas of
Slip2D; of it only the light ink ``#202020`` belongs here, and is checked.

The sheet, the palette and the icon caches are put back after every test
(rule 5), and every key registered is unregistered.
"""
from __future__ import annotations

import contextlib
import re
from collections import Counter

from PySide6.QtWidgets import QApplication

_THRESHOLD = 4.0


def _app():
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _themed():
    """The application, with its sheet, its palette and the icon caches put
    back afterwards."""
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


def _lum(c):
    def ch(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def _ratio(a, b):
    """The WCAG contrast ratio of two colours."""
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _rgb(name):
    from PySide6.QtGui import QColor
    c = QColor(name)
    return (c.red(), c.green(), c.blue())


def _background(qss, selector):
    """The ``background-color`` of the first rule of ``selector``."""
    m = re.search(re.escape(selector) + r"\s*\{[^}]*?background-color:\s*"
                  r"(#[0-9a-fA-F]{6})", qss)
    assert m, selector
    return m.group(1)


#: The roles that are text a widget writes (``disabled`` is pale on
#: purpose; the backgrounds, the grid and the separator are not text).
_TEXT_ROLES = ("muted", "muted_strong", "muted_soft", "error", "warning",
               "caution", "accent", "ink", "status_text", "toggle_off")


# ----------------------------------------------------------------------
class TestTheRoles:
    def test_the_light_colours_are_the_old_literals(self):
        from ogr_ui.themes import ROLE_COLORS
        light = ROLE_COLORS["light"]
        # what the widgets wrote before v0.1.316, role by role
        for role, literal in (("muted", "#555555"), ("muted_strong", "#444444"),
                              ("muted_soft", "#666666"),
                              ("disabled", "#909090"), ("error", "#b00020"),
                              ("warning", "#a05a00"), ("caution", "#8a5a00"),
                              ("accent", "#c0392b"), ("ink", "#202020"),
                              ("note_bg", "#f4f4f8"), ("info_bg", "#eeeeff"),
                              ("status_text", "#4a4a4a"),
                              ("toggle_off", "#707070"),
                              ("separator", "#c0c0c0"),
                              ("canvas_bg", "#fafafa"),
                              ("canvas_bg_gray", "#e8e8e8"),
                              ("grid_minor", "#dcdcdc"),
                              ("grid_major", "#b4b4b4"),
                              ("ruler_text", "#646464")):
            assert light[role] == literal, role

    def test_both_themes_have_the_same_roles(self):
        from ogr_ui.themes import ROLE_COLORS, THEMES
        assert set(ROLE_COLORS) == set(THEMES) == {"light", "dark"}
        assert set(ROLE_COLORS["dark"]) == set(ROLE_COLORS["light"])
        # and the dark one is a theme of its own, not a copy
        differ = [r for r in ROLE_COLORS["light"]
                  if ROLE_COLORS["light"][r] != ROLE_COLORS["dark"][r]]
        assert len(differ) == len(ROLE_COLORS["light"]), differ

    def test_every_text_role_reads_where_it_is_written(self):
        """On the window and on the status bar of its own theme, read from
        the sheet (the backgrounds those texts are written on)."""
        from ogr_ui.themes import ROLE_COLORS, THEMES
        low = []
        for theme, qss in THEMES.items():
            for where in ("QMainWindow, QDialog", "QStatusBar"):
                bg = _rgb(_background(qss, where))
                for role in _TEXT_ROLES:
                    r = _ratio(_rgb(ROLE_COLORS[theme][role]), bg)
                    if r < _THRESHOLD:
                        low.append((theme, where, role, round(r, 2)))
        assert low == [], low

    def test_theme_color_by_name(self):
        from ogr_ui.themes import ROLE_COLORS, theme_color
        for theme in ("light", "dark"):
            for role, value in ROLE_COLORS[theme].items():
                assert theme_color(role, theme) == value, (theme, role)
        # an unknown theme reads the light one; an unknown role is an error
        assert theme_color("ink", "sepia") == ROLE_COLORS["light"]["ink"]
        try:
            theme_color("no_such_role", "light")
        except KeyError:
            pass
        else:
            raise AssertionError("an unknown role gave a colour")


class TestTheActiveTheme:
    def test_it_is_read_from_the_sheet(self):
        """Not from a variable: a test that puts the sheet back must not
        leave the colours of the dark theme behind."""
        from ogr_ui.themes import THEMES, apply_theme, current_theme, theme_color
        with _themed() as app:
            apply_theme(app, "dark")
            assert current_theme() == "dark"
            assert current_theme(app) == "dark"
            assert theme_color("ink") == "#e0e0e0"
            app.setStyleSheet("")
            assert current_theme() == "light"
            # D350: the light ink is exactly the stored default colour
            assert theme_color("ink") == "#202020"
            # a sheet of somebody else's is no theme of ours
            app.setStyleSheet(THEMES["dark"] + "\nQLabel { color: red; }")
            assert current_theme() == "light"


class TestApplyTheme:
    def test_dark_sets_its_sheet_and_a_palette_whose_texts_read(self):
        from PySide6.QtGui import QPalette
        from ogr_ui.themes import THEMES, apply_theme
        with _themed() as app:
            apply_theme(app, "dark")
            assert app.styleSheet() == THEMES["dark"]
            p = app.palette()
            assert p.color(QPalette.Window).name() == "#2b2b2b"
            for text, ground in ((QPalette.WindowText, QPalette.Window),
                                 (QPalette.Text, QPalette.Base),
                                 (QPalette.ButtonText, QPalette.Button),
                                 (QPalette.ToolTipText, QPalette.ToolTipBase),
                                 (QPalette.HighlightedText,
                                  QPalette.Highlight)):
                r = _ratio(_rgb(p.color(text).name()),
                           _rgb(p.color(ground).name()))
                assert r >= _THRESHOLD, (text, ground, r)
            # a disabled text is paler than an enabled one, as in the sheet
            for role in (QPalette.WindowText, QPalette.Text,
                         QPalette.ButtonText):
                assert p.color(QPalette.Disabled, role).name() == "#7a7a7a"

    def test_light_puts_back_the_palette_before_any_theme(self):
        from PySide6.QtGui import QPalette
        from ogr_ui import themes
        with _themed() as app:
            before = QPalette(themes._ORIGINAL_PALETTE
                              if themes._ORIGINAL_PALETTE is not None
                              else app.palette())
            themes.apply_theme(app, "dark")
            assert app.palette() != before
            themes.apply_theme(app, "light")
            assert app.palette() == before
            # the palette, not the sheet: the light theme is a sheet of its
            # own, and putting back the one before is the caller's
            assert app.styleSheet() == themes.THEMES["light"]

    def test_an_unknown_name_is_the_light_theme(self):
        from PySide6.QtGui import QPalette
        from ogr_ui import themes
        with _themed() as app:
            themes.apply_theme(app, "dark")
            themes.apply_theme(app, "sepia")
            assert app.styleSheet() == themes.THEMES["light"]
            assert app.palette() == QPalette(themes._ORIGINAL_PALETTE)

    def test_it_installs_the_button_floor(self):
        from ogr_ui import button_floor
        from ogr_ui.themes import apply_theme
        with _themed() as app:
            apply_theme(app, "light")
            assert button_floor._floor is not None
            assert button_floor.install(app) is button_floor._floor

    def test_it_forgets_the_icons_built(self):
        from ogr_ui.resources.icons import icon
        from ogr_ui.themes import apply_theme
        with _themed() as app:
            icon("save")
            assert icon.cache_info().currsize >= 1
            apply_theme(app, "dark")
            assert icon.cache_info().currsize == 0


class TestADisabledEntryLooksDisabled:
    """D289: with a sheet, Qt draws a disabled item in the colour given to
    QMenu unless a ``:disabled`` rule says otherwise."""

    @staticmethod
    def _contrast(img, rect, bg) -> int:
        """Largest colour distance from ``bg`` inside ``rect``: the text."""
        best = 0
        for y in range(rect.top(), rect.bottom() + 1):
            for x in range(rect.left(), rect.right() + 1):
                c = img.pixelColor(x, y)
                best = max(best, abs(c.red() - bg.red())
                           + abs(c.green() - bg.green())
                           + abs(c.blue() - bg.blue()))
        return best

    def _rendered(self, theme):
        from PySide6.QtGui import QAction
        from PySide6.QtWidgets import QMenu
        from ogr_ui.themes import apply_theme
        with _themed() as app:
            apply_theme(app, theme)
            menu = QMenu()
            try:
                on = QAction("Compute Groundwater", menu)
                off = QAction("Compute Groundwater", menu)
                off.setEnabled(False)
                menu.addAction(on)
                menu.addAction(off)
                menu.popup(menu.mapToGlobal(menu.pos()))
                app.processEvents()
                img = menu.grab().toImage()
                r_on, r_off = menu.actionGeometry(on), menu.actionGeometry(off)
                bg = img.pixelColor(r_on.right() - 2, r_on.center().y())
                return (self._contrast(img, r_on, bg),
                        self._contrast(img, r_off, bg))
            finally:
                menu.hide()
                menu.deleteLater()
                app.processEvents()

    def test_light_draws_a_disabled_item_paler(self):
        on, off = self._rendered("light")
        assert off < 0.75 * on, (on, off)

    def test_dark_draws_a_disabled_item_paler(self):
        on, off = self._rendered("dark")
        assert off < 0.75 * on, (on, off)

    def test_every_coloured_widget_has_a_disabled_colour(self):
        from ogr_ui.themes import THEMES
        exempt = {"QMainWindow", "QDialog", "QMenuBar", "QStatusBar",
                  "QDockWidget", "QDockWidget::title", "QToolTip",
                  "QStatusBar QLabel"}
        for name, qss in THEMES.items():
            blocks = re.findall(r"([^{}]+)\{([^}]*)\}",
                                re.sub(r"/\*.*?\*/", "", qss, flags=re.S))
            coloured, disabled = set(), set()
            for sels, body in blocks:
                has_colour = re.search(r"(^|[;\s])color\s*:", body) is not None
                for sel in (s.strip() for s in sels.split(",")):
                    if sel.endswith(":disabled") and has_colour:
                        disabled.add(sel[:-len(":disabled")])
                    elif has_colour and ":" not in sel.replace("::", ""):
                        coloured.add("QMenu::item" if sel == "QMenu" else sel)
            # the census has to see something to mean anything
            assert len(coloured) >= 3, (name, coloured)
            missing = sorted(s for s in coloured - exempt if s not in disabled)
            assert not missing, (name, missing)

    def test_the_dark_disabled_header_reads(self):
        """D319: a disabled header sits on #404040, where the shared grey
        #7a7a7a is 2.4:1; the last rule for it wins."""
        from ogr_ui.themes import _DARK
        rules = re.findall(r"QHeaderView::section:disabled\s*\{\s*color:\s*"
                           r"(#[0-9a-fA-F]{6})", _DARK)
        assert rules, "no rule of its own"
        header = _background(_DARK, "QHeaderView::section")
        assert _ratio(_rgb(rules[-1]), _rgb(header)) >= _THRESHOLD
        # control: the shared grey would not
        assert _ratio(_rgb("#7a7a7a"), _rgb(header)) < _THRESHOLD


# ----------------------------------------------------------------------
def _icon_ink(qicon):
    """The commonest colour of the opaque pixels of an icon."""
    img = qicon.pixmap(24, 24).toImage()
    px = [img.pixelColor(x, y) for y in range(img.height())
          for x in range(img.width())]
    solid = [(c.red(), c.green(), c.blue()) for c in px if c.alpha() > 200]
    assert solid, "an empty icon"
    return Counter(solid).most_common(1)[0][0]


class TestTheIcons:
    def test_an_icon_with_no_colour_of_its_own_reads_on_the_dark_menu(self):
        from ogr_ui.resources.icons import icon
        from ogr_ui.themes import _DARK, apply_theme
        menu_bg = _rgb(_background(_DARK, "QMenu"))
        with _themed() as app:
            apply_theme(app, "dark")
            ink = _icon_ink(icon("open_project"))
            assert _ratio(ink, menu_bg) >= 3.0, ink
            # and the dark grey of the External boundary is lifted
            ink = _icon_ink(icon("ext_boundary"))
            assert _ratio(ink, menu_bg) >= 3.0, ink

    def test_a_change_of_theme_builds_them_again(self):
        """Without ``reset_cache`` the cached light icon would come back
        under the dark theme."""
        from ogr_ui.resources.icons import icon
        from ogr_ui.themes import apply_theme
        with _themed() as app:
            apply_theme(app, "light")
            light = _icon_ink(icon("open_project"))
            apply_theme(app, "dark")
            dark = _icon_ink(icon("open_project"))
            assert light != dark
            assert _lum(dark) > _lum(light)

    def test_reset_cache_forgets_them(self):
        from ogr_ui.resources import icons
        with _themed():
            icons.icon("save")
            icons.icon("undo")
            assert icons.icon.cache_info().currsize >= 2
            icons.reset_cache()
            assert icons.icon.cache_info().currsize == 0

    def test_stretch_support_is_not_the_eraser(self):
        """D355: it borrowed Delete Support's eraser."""
        from ogr_ui.resources import icons
        assert icons.has("stretch_support")
        assert icons._CATALOG["stretch_support"][0] != \
            icons._CATALOG["delete_support"][0]

    def test_has(self):
        from ogr_ui.resources.icons import has
        assert has("block_object")
        # v0.1.168: the three-point surface has no icon of its own
        assert not has("surface_3pts")


class TestForTheTheme:
    def test_the_light_theme_keeps_every_colour(self):
        from ogr_ui.resources.icons import _for_theme
        with _themed() as app:
            app.setStyleSheet("")
            assert _for_theme(None) is None
            for colour in ("#2c2c2c", "#4b0082", "#1e90ff", "#c0392b"):
                assert _for_theme(colour) == colour

    def test_the_dark_theme_lifts_the_dark_ones(self):
        from PySide6.QtGui import QColor
        from ogr_ui.resources.icons import _for_theme
        from ogr_ui.themes import THEMES
        with _themed() as app:
            app.setStyleSheet(THEMES["dark"])
            assert _for_theme(None) is None
            # light enough already: kept
            assert _for_theme("#1e90ff") == "#1e90ff"
            # a dark grey becomes the palette's text colour
            assert _for_theme("#2c2c2c") is None
            # a dark saturated one keeps its hue, lighter
            lifted = QColor(_for_theme("#4b0082"))
            dark = QColor("#4b0082")
            assert lifted.lightnessF() > dark.lightnessF()
            assert lifted.lightnessF() >= 0.35
            assert abs(lifted.hslHue() - dark.hslHue()) <= 2


class TestAProgramsOwnKeys:
    KEYS = {"ogr_ui_test_alpha": ("fa6s.anchor", None),
            "ogr_ui_test_beta": ("fa6s.bug", "#123456")}

    def test_register_adds_them_and_unregister_takes_them_away(self):
        from ogr_ui.resources import icons
        try:
            icons.register(self.KEYS)
            for key, entry in self.KEYS.items():
                assert icons.has(key), key
                assert icons._CATALOG[key] == entry
            # a key of its own is drawn as its own, not as the gear an
            # unknown key gets
            with _themed():
                own = icons.icon("ogr_ui_test_alpha").pixmap(24, 24).toImage()
                gear = icons.icon("ogr_ui_test_no_such").pixmap(
                    24, 24).toImage()
                assert own != gear
        finally:
            icons.unregister(self.KEYS)
        for key in self.KEYS:
            assert not icons.has(key), key

    def test_a_key_of_the_suite_is_refused_and_none_is_added(self):
        from ogr_ui.resources import icons
        before = dict(icons._CATALOG)
        try:
            try:
                icons.register({"ogr_ui_test_alpha": ("fa6s.anchor", None),
                                "save": ("fa6s.bug", None)})
            except ValueError as e:
                assert "save" in str(e), e
            else:
                raise AssertionError("a key of the suite was taken")
            assert icons._CATALOG == before
            assert not icons.has("ogr_ui_test_alpha")
        finally:
            icons.unregister(["ogr_ui_test_alpha"])

    def test_register_and_unregister_forget_the_icons_built(self):
        from ogr_ui.resources import icons
        with _themed():
            try:
                icons.icon("save")
                assert icons.icon.cache_info().currsize >= 1
                icons.register(self.KEYS)
                assert icons.icon.cache_info().currsize == 0
                icons.icon("ogr_ui_test_alpha")
                assert icons.icon.cache_info().currsize >= 1
            finally:
                icons.unregister(self.KEYS)
            assert icons.icon.cache_info().currsize == 0


class TestASuiteKeyCannotBeRemoved:
    """OGR GUI 0.1.0 — ``unregister`` refuses the suite's own keys, as
    ``register`` refuses to redefine them (found porting these tests: it
    removed any key it was given)."""

    def test_a_suite_key_is_refused_and_stays(self):
        from ogr_ui.resources import icons
        try:
            icons.unregister(["save"])
        except ValueError as exc:
            assert "save" in str(exc)
        else:
            raise AssertionError("unregister removed a key of the suite")
        assert icons.has("save")
