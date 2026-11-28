# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.0 — the contour engine (``ogr_ui.contours``) and the Contour
Options dialog (``ogr_ui.dialogs.contour_options_dialog``).

The invariants:

* **banded, not smooth, by default**: every value inside a band gets
  exactly the same colour, and a discrete palette whose stop count matches
  the intervals is indexed, never interpolated, so the measured colours of
  the 24-band rainbow are the colours drawn;
* **clamping, not discarding**: a value outside the range keeps the end
  colour, and the top band is labelled with a trailing ``+``;
* **auto-range ignores outliers** and keeps the low end as it is;
* **a field says where it starts**: a :class:`ContourField` with a
  ``start`` begins (and goes back with *Restore Defaults*) to those
  settings, one without it to :meth:`ContourSettings.automatic`; and a
  :class:`RangePreset` is one button that sets the bounds and intervals
  once and turns the automatic range off;
* **no setting does nothing** (rule 7): every control of the dialog, and
  every preset button, moves the settings the dialog collects.

What changed on the way out of OGR Slip2D: ``SCALAR_FIELDS``,
``available_fields`` and ``ContourSettings.for_field`` (the factor of
safety's fixed 0-6 range) stayed in that program. The dialog takes
``fields`` (a list of :class:`ContourField`) and ``presets`` (a list of
:class:`RangePreset`, one button each) where it had Slip2D's field keys and
its «0 to 6» button. The tests below declare a field and a preset of their
own in place of the factor of safety.

Ported from OGR Slip2D (v0.1.486):

* ``tests/test_contours_i2_v150.py`` (v0.1.50, Interpret phase I2): the
  palette, banding, range, auto-range, formatting and dialog tests, every
  one. Left out: ``TestAvailableFields`` (``available_fields`` and
  ``SCALAR_FIELDS`` stayed in Slip2D) and ``TestInterpretIntegration`` (it
  needs the interpret window and the limit-equilibrium engine).
* ``tests/test_slide_legend_v182.py`` (v0.1.82): ``TestTheMeasuredPalette``
  and ``TestRangePolicyPerField``, on a 0-6 field the test declares instead
  of ``for_field("fos")``. ``TestSurfacesCarryTheLegendColour`` needs the
  interpret window and stays; its legend checks are in
  ``test_legend_v010.py``.
* ``tests/test_interpret_i3_v153.py`` (v0.1.53, phase I3): the one contour
  invariant that needs no window, that two scalars keep separate settings
  (``test_groundwater_contours_are_separate``), here on two fields'
  defaults. The rest of that file is the interpret window's menus.
"""
from __future__ import annotations

import contextlib

from ogr_ui.contours import (
    DEFAULT_PALETTE,
    DISCRETE_PALETTES,
    PALETTES,
    ContourField,
    ContourMode,
    ContourSettings,
    RangePreset,
    sample_palette,
)

# Sampled from the reference legend, top (0.000) to bottom (6.000+).
_MEASURED = [
    "#ff0000", "#ff2a00", "#ff5500", "#ff7f00", "#ffaa00", "#ffd400",
    "#feff00", "#d4ff00", "#a9ff00", "#7fff00", "#55ff00", "#2aff00",
    "#00ff00", "#00ff2a", "#00ff54", "#00ff7f", "#00ffa9", "#00ffd4",
    "#00ffff", "#00d4ff", "#00a9ff", "#007fff", "#0054ff", "#0000ff",
]

#: A field with a fixed 0-6 range in 24 bands, as a program declares one
#: (OGR Slip2D's factor of safety is such a field).
_RATIO = ContourField("ratio", "Ratio",
                      start=ContourSettings(vmin=0.0, vmax=6.0,
                                            intervals=24))
#: A field with no fixed range: it starts automatic.
_HEAD = ContourField("head", "Head")
#: A one-click range, as a program declares one (Slip2D's «0 to 6»).
_ZERO_TO_SIX = RangePreset("0 to 6", 0.0, 6.0, 24,
                           tooltip="The fixed range of the ratio.")
_ONE_TO_TWO = RangePreset("1 to 2", 1.0, 2.0, 5)


def _is_hex(c) -> bool:
    return (isinstance(c, str) and c.startswith("#") and len(c) == 7
            and all(ch in "0123456789abcdefABCDEF" for ch in c[1:]))


# ======================================================================
# Ported from Slip2D tests/test_contours_i2_v150.py
# ======================================================================
class TestPalettes:
    def test_every_palette_has_stops(self):
        for name, stops in PALETTES.items():
            assert stops, name
            assert all(_is_hex(c) for c in stops), name

    def test_default_palette_exists(self):
        assert DEFAULT_PALETTE in PALETTES

    def test_sampling_returns_the_end_stops(self):
        for name, stops in PALETTES.items():
            assert sample_palette(name, 0.0).lower() == stops[0].lower()
            assert sample_palette(name, 1.0).lower() == stops[-1].lower()

    def test_sampling_interpolates(self):
        mid = sample_palette("Greyscale", 0.5)
        assert _is_hex(mid)
        assert mid.lower() not in [c.lower()
                                   for c in PALETTES["Greyscale"][:1]]

    def test_out_of_range_is_clamped(self):
        assert sample_palette("Viridis", -5.0) == \
            sample_palette("Viridis", 0.0)
        assert sample_palette("Viridis", 5.0) == \
            sample_palette("Viridis", 1.0)

    def test_unknown_palette_falls_back(self):
        assert _is_hex(sample_palette("does-not-exist", 0.5))

    def test_accessible_palette_offered(self):
        """A report may have to remain readable in print and to readers
        with colour vision deficiency."""
        assert "Accessible" in PALETTES
        assert "Greyscale" in PALETTES


class TestBanding:
    def test_values_in_one_band_share_a_colour(self):
        """This is what makes a contour plot readable: a band is one
        colour, so a reader can match it against the legend."""
        s = ContourSettings(vmin=0.0, vmax=1.0, intervals=4)
        a = s.colour_for(0.01)
        b = s.colour_for(0.24)
        assert a == b
        assert s.colour_for(0.26) != a

    def test_smooth_mode_does_not_band(self):
        s = ContourSettings(vmin=0.0, vmax=1.0, intervals=4,
                            mode=ContourMode.SMOOTH)
        assert s.colour_for(0.01) != s.colour_for(0.24)

    def test_level_boundaries(self):
        s = ContourSettings(vmin=1.0, vmax=2.0, intervals=4)
        lv = s.levels()
        assert len(lv) == 5
        assert abs(lv[0] - 1.0) < 1e-12
        assert abs(lv[-1] - 2.0) < 1e-12
        assert abs(lv[1] - 1.25) < 1e-12

    def test_band_colours_count(self):
        s = ContourSettings(intervals=7)
        assert len(s.band_colours()) == 7
        assert all(_is_hex(c) for c in s.band_colours())

    def test_level_index_bounds(self):
        s = ContourSettings(vmin=0.0, vmax=1.0, intervals=5)
        assert s.level_index(-10.0) == 0
        assert s.level_index(10.0) == 4
        assert 0 <= s.level_index(0.5) <= 4


class TestRangeHandling:
    def test_values_outside_the_range_are_clamped(self):
        """Narrowing the range to study a detail must not blank out the
        rest of the model."""
        s = ContourSettings(vmin=1.0, vmax=2.0, intervals=4)
        assert s.colour_for(-100.0) == s.colour_for(1.0)
        assert s.colour_for(100.0) == s.colour_for(1.999)

    def test_degenerate_range_does_not_divide_by_zero(self):
        s = ContourSettings(vmin=1.5, vmax=1.5)
        assert s.span > 0
        assert _is_hex(s.colour_for(1.5))

    def test_non_finite_value_is_safe(self):
        s = ContourSettings()
        assert _is_hex(s.colour_for(float("nan")))
        assert _is_hex(s.colour_for(float("inf")))

    def test_reverse_flips_the_mapping(self):
        a = ContourSettings(vmin=0.0, vmax=1.0, mode=ContourMode.SMOOTH)
        b = ContourSettings(vmin=0.0, vmax=1.0, mode=ContourMode.SMOOTH,
                            reverse=True)
        assert a.colour_for(0.0) == b.colour_for(1.0)
        assert a.colour_for(1.0) == b.colour_for(0.0)


class TestAutoRange:
    def test_ignores_extreme_outliers(self):
        """One value at 40 must not squash the rest into a single band."""
        values = [1.0 + 0.01 * i for i in range(100)] + [40.0]
        s = ContourSettings()
        s.fit_to(values)
        assert s.vmin <= 1.0
        assert s.vmax < 5.0, s.vmax

    def test_keeps_the_low_end_exactly(self):
        """The low end is taken as-is rather than trimmed."""
        values = [0.7, 1.0, 1.5, 2.0]
        s = ContourSettings()
        s.fit_to(values)
        assert abs(s.vmin - 0.7) < 1e-12

    def test_constant_data_gives_a_usable_range(self):
        s = ContourSettings()
        s.fit_to([2.0] * 20)
        assert s.vmax > s.vmin

    def test_empty_data_leaves_the_range_alone(self):
        s = ContourSettings(vmin=0.0, vmax=3.0)
        s.fit_to([])
        assert (s.vmin, s.vmax) == (0.0, 3.0)


class TestFormattingAndSerialisation:
    def test_decimal_and_scientific(self):
        s = ContourSettings(decimals=3)
        assert s.format_value(0.5) == "0.500"
        s.scientific = True
        assert "e" in s.format_value(0.5)

    def test_round_trip(self):
        s = ContourSettings(mode=ContourMode.LINES, palette="Viridis",
                            vmin=0.5, vmax=4.0, intervals=12,
                            reverse=True, field="pore_pressure",
                            decimals=3, scientific=True, opacity=0.4)
        s2 = ContourSettings.from_dict(s.to_dict())
        assert s2.mode == ContourMode.LINES
        assert s2.palette == "Viridis"
        assert s2.intervals == 12
        assert s2.reverse is True
        assert s2.field == "pore_pressure"
        assert s2.opacity == 0.4
        assert s2 == s
        assert s2.colour_for(2.0) == s.colour_for(2.0)


# ======================================================================
# Ported from Slip2D tests/test_slide_legend_v182.py, on a field of the
# test's own (Slip2D's for_field("fos") stayed in Slip2D)
# ======================================================================
class TestTheMeasuredPalette:
    def test_the_palette_is_the_measurement(self):
        assert list(PALETTES["Rainbow (24 bands)"]) == _MEASURED

    def test_it_is_the_default(self):
        assert DEFAULT_PALETTE == "Rainbow (24 bands)"
        s = _RATIO.defaults()
        assert s.palette == "Rainbow (24 bands)"
        assert (s.vmin, s.vmax, s.intervals) == (0.0, 6.0, 24)

    def test_bands_are_indexed_not_interpolated(self):
        """A 24-stop ramp sampled at band centres lands halfway between
        every pair of measured colours, so none of the reference colours
        would ever actually be drawn. Discrete palettes are indexed."""
        assert "Rainbow (24 bands)" in DISCRETE_PALETTES
        s = _RATIO.defaults()
        # Band i covers [0.25 i, 0.25 (i+1)).
        for i, want in enumerate(_MEASURED):
            v = 0.25 * i + 0.125
            assert s.colour_for(v).lower() == want, (i, v, s.colour_for(v))

    def test_with_other_intervals_it_is_sampled(self):
        """Indexing only applies when the bands ARE the stops."""
        s = ContourSettings(vmin=0.0, vmax=6.0, intervals=12)
        assert len(set(s.band_colours())) == 12
        assert any(c not in _MEASURED for c in s.band_colours())

    def test_the_low_end_is_red_and_the_high_end_is_not(self):
        s = _RATIO.defaults()
        assert s.colour_for(0.10).lower() == "#ff0000"
        assert s.colour_for(0.883).lower().startswith("#ff")
        # 5.6 falls in band 22 (5.50–5.75); 5.9 is already in the last.
        assert s.colour_for(5.6).lower() == "#0054ff"

    def test_everything_above_the_top_shares_the_last_band(self):
        s = _RATIO.defaults()
        assert s.colour_for(6.0) == s.colour_for(31.34)
        assert s.colour_for(6.0).lower() == "#0000ff"

    def test_the_last_label_says_it_saturates(self):
        """Labelling the top boundary "6.000" would claim the scale stops
        there when in fact everything above it is drawn the same."""
        s = _RATIO.defaults()
        assert s.band_label(0) == "0.000"
        assert s.band_label(2) == "0.500"
        assert s.band_label(24) == "6.000+"


class TestRangePolicyPerField:
    def test_a_field_with_a_start_does_not_auto_range(self):
        assert _RATIO.defaults().auto_range is False

    def test_a_field_without_one_does(self):
        """A total head in metres has no natural fixed range, and no one
        value would suit two models."""
        s = _HEAD.defaults()
        assert s.auto_range is True
        assert s.palette != "Rainbow (24 bands)"
        assert s == ContourSettings.automatic("head")

    def test_the_same_value_is_always_the_same_colour(self):
        """What a fixed range buys: with auto-range the scale is rebuilt
        from whatever the current result contains, so the same value comes
        out in different colours on two runs."""
        run_a = [0.88 + 0.01 * i for i in range(40)]
        run_b = run_a + [4.0 + 0.5 * i for i in range(30)]
        a, b = ContourSettings(auto_range=True), ContourSettings(
            auto_range=True)
        a.fit_to(run_a)
        b.fit_to(run_b)
        probes = [1.00, 1.10, 1.20]
        assert any(a.colour_for(v) != b.colour_for(v) for v in probes), (
            [(a.colour_for(v), b.colour_for(v)) for v in probes])

        fa, fb = _RATIO.defaults(), _RATIO.defaults()
        assert fa.auto_range is False and fb.auto_range is False
        assert all(fa.colour_for(v) == fb.colour_for(v)
                   for v in probes + [0.883])


# ======================================================================
# The new interface: ContourField, RangePreset, automatic()
# ======================================================================
class TestContourField:
    def test_defaults_carry_the_key(self):
        start = ContourSettings(vmin=1.0, vmax=3.0, field="something else")
        f = ContourField("k", "K", start=start)
        assert f.defaults().field == "k"
        assert (f.defaults().vmin, f.defaults().vmax) == (1.0, 3.0)

    def test_defaults_are_a_fresh_copy(self):
        """Editing what a field starts from must not change where it
        starts the next time (or Restore Defaults would restore the edit)."""
        a = _RATIO.defaults()
        a.vmax = 99.0
        a.palette = "Viridis"
        b = _RATIO.defaults()
        assert a is not b
        assert (b.vmax, b.palette) == (6.0, "Rainbow (24 bands)")
        assert _RATIO.start.vmax == 6.0

    def test_two_fields_keep_separate_settings(self):
        """Two scalars are different quantities with different ranges;
        one shared settings object would make both useless (Slip2D
        test_interpret_i3_v153, test_groundwater_contours_are_separate)."""
        ratio, head = _RATIO.defaults(), _HEAD.defaults()
        assert ratio is not head
        assert ratio.field != head.field
        head.vmin = -50.0
        assert _RATIO.defaults().vmin == 0.0

    def test_automatic(self):
        s = ContourSettings.automatic("head")
        assert s.field == "head"
        assert s.auto_range is True
        # 0.2.0: Viridis, as OGR Slip2D 0.1.506 (until then «Hot to cold»)
        assert s.palette == "Viridis" and s.palette in PALETTES
        assert s.intervals == 8
        assert s.decimals == 2

    def test_the_field_palette_grows_in_lightness(self):
        """0.2.0 -- the palette a field starts from reads in grey: its CIE
        1976 L* grows from stop to stop (sRGB to linear, the D65 Y, then
        L* = 116 f(Y) - 16, written out here and not taken from the code)."""
        from ogr_ui.contours import FIELD_PALETTE

        def lightness(hex_colour):
            def linear(c):
                c /= 255.0
                return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
            r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
            y = 0.2126 * linear(r) + 0.7152 * linear(g) + 0.0722 * linear(b)
            f = y ** (1 / 3) if y > (6 / 29) ** 3 else y / (3 * (6 / 29) ** 2) + 4 / 29
            return 116 * f - 16

        assert FIELD_PALETTE == "Viridis"
        ls = [lightness(c) for c in PALETTES[FIELD_PALETTE]]
        assert all(b > a for a, b in zip(ls, ls[1:])), ls
        assert ls[0] < 20 and ls[-1] > 85, ls


# ======================================================================
# The dialog (from Slip2D TestDialog, with fields and presets of its own)
# ======================================================================
def _app():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _dialog(settings=None, fields=(_RATIO, _HEAD), values=None,
            presets=(_ZERO_TO_SIX,), language="en"):
    """A Contour Options dialog, in ``language``, deleted afterwards."""
    import shiboken6
    from ogr_ui.dialogs.contour_options_dialog import ContourOptionsDialog
    from ogr_ui.i18n import current_language, set_language
    _app()
    before = current_language()
    settings = _RATIO.defaults() if settings is None else settings
    try:
        set_language(language)
        d = ContourOptionsDialog(settings, fields,
                                 [1.0, 1.5, 2.0, 2.5] if values is None
                                 else values, presets, None)
        try:
            yield d
        finally:
            if shiboken6.isValid(d):
                shiboken6.delete(d)
    finally:
        set_language(before)


class TestDialog:
    def test_offers_every_mode_and_palette(self):
        with _dialog() as d:
            assert d.cbo_mode.count() == 5
            assert d.cbo_palette.count() == len(PALETTES)

    def test_auto_range_disables_the_bounds(self):
        with _dialog() as d:
            d.chk_auto.setChecked(True)
            assert d.sp_min.isEnabled() is False
            d.chk_auto.setChecked(False)
            assert d.sp_min.isEnabled() is True

    def test_auto_range_fits_the_data(self):
        with _dialog(values=[2.0, 2.5, 3.0]) as d:
            d.chk_auto.setChecked(False)
            d.chk_auto.setChecked(True)
            assert abs(d.sp_min.value() - 2.0) < 1e-6

    def test_interval_size_is_reported(self):
        with _dialog() as d:
            d.chk_auto.setChecked(False)
            d.sp_min.setValue(0.0)
            d.sp_max.setValue(1.0)
            d.sp_int.setValue(4)
            assert d.lbl_step.text().startswith("0.25")

    def test_preview_follows_the_settings(self):
        with _dialog() as d:
            before = d.preview._settings.palette
            d.cbo_palette.setCurrentIndex(d.cbo_palette.findData("Viridis"))
            assert d.preview._settings.palette == "Viridis" != before

    def test_accept_collects_everything(self):
        with _dialog() as d:
            d.chk_auto.setChecked(False)
            d.sp_int.setValue(11)
            d.chk_rev.setChecked(True)
            d.cbo_mode.setCurrentIndex(d.cbo_mode.findData(ContourMode.LINES))
            d._accept()
            assert d.settings.intervals == 11
            assert d.settings.reverse is True
            assert d.settings.mode == ContourMode.LINES

    def test_defaults_restore(self):
        with _dialog() as d:
            d.sp_int.setValue(30)
            d._defaults()
            assert d.sp_int.value() == _RATIO.defaults().intervals


class TestDialogFieldsAndPresets:
    def test_offers_each_field_by_its_label(self):
        with _dialog() as d:
            keys = [d.cbo_field.itemData(i) for i in range(d.cbo_field.count())]
            texts = [d.cbo_field.itemText(i)
                     for i in range(d.cbo_field.count())]
            assert keys == ["ratio", "head"]
            assert texts == ["Ratio", "Head"]

    def test_opens_on_the_field_of_the_settings(self):
        with _dialog(settings=_HEAD.defaults()) as d:
            assert d.cbo_field.currentData() == "head"

    def test_switching_field_resets_the_range(self):
        """A 0-6 range means everything for one scalar and nothing for
        another: the bounds follow the field."""
        with _dialog(values=[]) as d:
            d.sp_min.setValue(2.0)
            d.sp_max.setValue(3.0)
            d.cbo_field.setCurrentIndex(d.cbo_field.findData("head"))
            head = _HEAD.defaults()
            assert d.chk_auto.isChecked() is True
            assert d.sp_int.value() == head.intervals
            assert d.cbo_palette.currentData() == head.palette
            d.cbo_field.setCurrentIndex(d.cbo_field.findData("ratio"))
            assert (d.sp_min.value(), d.sp_max.value()) == (0.0, 6.0)
            assert d.chk_auto.isChecked() is False

    def test_values_fit_only_the_field_they_came_from(self):
        """The sample values belong to the field the dialog opened on:
        fitting them to another would fit one quantity to another's
        numbers."""
        with _dialog(settings=_HEAD.defaults(),
                     values=[10.0, 20.0, 30.0]) as d:
            assert d.btn_fit.isEnabled() is True
            d.cbo_field.setCurrentIndex(d.cbo_field.findData("ratio"))
            assert d.btn_fit.isEnabled() is False
            before = (d.sp_min.value(), d.sp_max.value())
            d._range_fit()
            assert (d.sp_min.value(), d.sp_max.value()) == before
            d.cbo_field.setCurrentIndex(d.cbo_field.findData("head"))
            # back on its own field, the automatic start fits the values
            assert abs(d.sp_min.value() - 10.0) < 1e-6

    def test_no_values_no_fit(self):
        with _dialog(values=[]) as d:
            assert d.btn_fit.isEnabled() is False

    def test_no_fields_is_the_field_the_settings_name(self):
        with _dialog(settings=ContourSettings(field="other"), fields=(),
                     values=[]) as d:
            assert d.cbo_field.count() == 1
            assert d.cbo_field.currentData() == "other"
            d._defaults()
            # with no start, Restore Defaults is the automatic start
            assert d.chk_auto.isChecked() is True
            assert d.sp_int.value() == ContourSettings.automatic("x").intervals

    def test_one_button_per_preset(self):
        with _dialog(presets=(_ZERO_TO_SIX, _ONE_TO_TWO)) as d:
            assert [b.text() for b in d.preset_buttons] == ["0 to 6",
                                                            "1 to 2"]
            assert d.preset_buttons[0].toolTip() == _ZERO_TO_SIX.tooltip
            assert d.preset_buttons[1].toolTip() == ""
        with _dialog(presets=()) as d:
            assert d.preset_buttons == []

    def test_a_preset_sets_its_range_once(self):
        with _dialog(presets=(_ZERO_TO_SIX, _ONE_TO_TWO)) as d:
            d.chk_auto.setChecked(True)
            d.preset_buttons[1].click()
            assert d.chk_auto.isChecked() is False
            assert (d.sp_min.value(), d.sp_max.value(),
                    d.sp_int.value()) == (1.0, 2.0, 5)
            d.preset_buttons[0].click()
            assert (d.sp_min.value(), d.sp_max.value(),
                    d.sp_int.value()) == (0.0, 6.0, 24)

    def test_labels_are_shown_through_tr(self):
        """The program adds the translation of its own labels; the dialog
        shows them through tr()."""
        from ogr_ui.i18n import _DICTS
        es = _DICTS["es"]
        added = {"Ratio": "Razón", "1 to 2": "De 1 a 2"}
        saved = {k: es.get(k) for k in added}
        es.update(added)
        try:
            with _dialog(presets=(_ONE_TO_TWO,), language="es") as d:
                assert d.cbo_field.itemText(0) == "Razón"
                assert d.preset_buttons[0].text() == "De 1 a 2"
        finally:
            for k, v in saved.items():
                if v is None:
                    es.pop(k, None)
                else:
                    es[k] = v

    def test_opacity_passes_through(self):
        """No control edits it, so the dialog must hand it back as it came,
        not reset it."""
        s = _RATIO.defaults()
        s.opacity = 0.35
        with _dialog(settings=s) as d:
            d._accept()
            assert d.settings.opacity == 0.35

    def test_the_settings_given_are_not_edited(self):
        s = _RATIO.defaults()
        with _dialog(settings=s) as d:
            d.sp_int.setValue(7)
            d._accept()
            assert d.settings is not s
            assert s.intervals == 24


class TestEveryControlMovesTheSettings:
    """Rule 7: every control of the dialog moves the settings it collects,
    and each collected setting moves what is drawn or written."""

    def _moves(self, change, field):
        with _dialog(values=[]) as d:
            d.chk_auto.setChecked(False)
            before = d._collect()
            change(d)
            after = d._collect()
            assert getattr(after, field) != getattr(before, field), field
            d._accept()
            assert getattr(d.settings, field) == getattr(after, field)

    def test_field(self):
        self._moves(lambda d: d.cbo_field.setCurrentIndex(
            d.cbo_field.findData("head")), "field")

    def test_automatic_range(self):
        self._moves(lambda d: d.chk_auto.setChecked(True), "auto_range")

    def test_minimum(self):
        self._moves(lambda d: d.sp_min.setValue(1.5), "vmin")

    def test_maximum(self):
        self._moves(lambda d: d.sp_max.setValue(4.5), "vmax")

    def test_intervals(self):
        self._moves(lambda d: d.sp_int.setValue(10), "intervals")

    def test_mode(self):
        self._moves(lambda d: d.cbo_mode.setCurrentIndex(
            d.cbo_mode.findData(ContourMode.SMOOTH)), "mode")

    def test_palette(self):
        self._moves(lambda d: d.cbo_palette.setCurrentIndex(
            d.cbo_palette.findData("Viridis")), "palette")

    def test_reverse(self):
        self._moves(lambda d: d.chk_rev.setChecked(True), "reverse")

    def test_decimals(self):
        self._moves(lambda d: d.sp_dec.setValue(5), "decimals")

    def test_scientific(self):
        self._moves(lambda d: d.chk_sci.setChecked(True), "scientific")

    def test_a_preset_button(self):
        with _dialog(presets=(_ONE_TO_TWO,), values=[]) as d:
            before = d._collect()
            d.preset_buttons[0].click()
            after = d._collect()
            assert (after.vmin, after.vmax, after.intervals) != \
                (before.vmin, before.vmax, before.intervals)

    def test_fit_to_results(self):
        with _dialog(values=[2.0, 2.5, 3.0]) as d:
            d.chk_auto.setChecked(False)
            before = d._collect()
            d.btn_fit.click()
            after = d._collect()
            assert after.vmin != before.vmin and after.vmax != before.vmax
            assert abs(after.vmin - 2.0) < 1e-6

    def test_each_setting_changes_a_colour_or_a_label(self):
        """And what the dialog collects is used: each of these changes the
        colour of some value or the text of a band. (``field`` and
        ``auto_range`` are the program's to act on: which values, and
        whether to fit them.)"""
        base = ContourSettings(vmin=0.0, vmax=6.0, intervals=24)
        probes = [0.1 * i for i in range(-5, 66)]

        def drawn(s):
            return ([s.colour_for(v) for v in probes],
                    [s.band_label(i) for i in range(s.intervals + 1)])

        changes = {
            "mode": ContourMode.SMOOTH, "palette": "Viridis",
            "vmin": 1.0, "vmax": 4.0, "intervals": 12, "reverse": True,
            "decimals": 1, "scientific": True,
        }
        for name, value in changes.items():
            s = ContourSettings.from_dict(base.to_dict())
            setattr(s, name, value)
            assert drawn(s) != drawn(base), name


class TestRestoreDefaultsIsTheFieldsStart:
    """OGR GUI 0.1.0 — *Restore Defaults* brings back every control of the
    field's start. Found porting these tests: the dialog wrote FILLED, not
    reversed, as constants, and left Scientific notation as it was, which in
    Slip2D was the same thing as its fields' start and here is not."""

    _ODD = ContourField("odd", "Odd", start=ContourSettings(
        mode=ContourMode.LINES, reverse=True, scientific=True,
        palette="Viridis", vmin=-1.0, vmax=1.0, intervals=4, decimals=1))

    def test_every_control_comes_back_to_the_start(self):
        with _dialog(settings=self._ODD.defaults(), fields=(self._ODD,)) as d:
            d.cbo_mode.setCurrentIndex(d.cbo_mode.findData(ContourMode.FILLED))
            d.chk_rev.setChecked(False)
            d.chk_sci.setChecked(False)
            d.cbo_palette.setCurrentIndex(d.cbo_palette.findData("Greyscale"))
            d.sp_int.setValue(10)
            d._defaults()
            got = d._collect()
            want = self._ODD.defaults()
            for name in ("mode", "reverse", "scientific", "palette", "vmin",
                         "vmax", "intervals", "decimals", "auto_range"):
                assert getattr(got, name) == getattr(want, name), name

    def test_an_automatic_field_turns_scientific_off_again(self):
        with _dialog(settings=_HEAD.defaults(), fields=(_HEAD,)) as d:
            d.chk_sci.setChecked(True)
            d._defaults()
            assert not d.chk_sci.isChecked()
