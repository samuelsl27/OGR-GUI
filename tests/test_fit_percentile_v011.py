# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.1 — the percentile of the fit, per field (spec 002).

OGR FEM2D asked for it (2026-11-24): the Contour Options dialog fitted
every field to its 98th percentile, which is right for a factor of safety
(one surface at 40 would squash every other into one band) and wrong for a
stress, whose peak at a tunnel wall is the very thing looked for. Each
:class:`ContourField` now says the share of the values its automatic
maximum covers, 0.98 unless the program says otherwise, and 1 for the
whole range.

The invariants:

* **the field declares it** and a wrong one is refused where it is
  declared, naming the field (RF-1, RF-2, RF-9);
* **the fit is an identity** (rule 1): the expected bounds are written by
  hand from the index ``round(p * (n - 1))`` of the sorted finite values,
  never computed with the function under test (RF-6);
* **the dialog fits with the chosen field's percentile** in its three
  fits -- *Fit to results*, the automatic-range checkbox and *Restore
  Defaults*, which also runs on a change of field -- and what it returns
  on OK carries it (rule 7) (RF-3, RF-4, RF-5);
* **a program that gives no percentile gets the 0.1.0 ranges** and the
  0.1.0 help (RF-10);
* **the help of the checkbox says what the chosen field does**: that the
  maximum uses a percentile, or that the range goes from the smallest
  value to the largest, in English and in Spanish, and it follows a
  change of field (RF-7, RF-8).

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import contextlib
import math

from ogr_ui.contours import ContourField, ContourSettings

# A hundred values 1.00, 1.01, ..., 1.99 and one peak of 50 (the test
# OGR FEM2D asked for). Sorted, n = 101; with 0.98 the index is
# round(0.98 * 100) = 98, the value 1.98; with 1 it is 100, the peak.
_PEAKED = [1.0 + i / 100 for i in range(100)] + [50.0]


def _fit(values, percentile):
    s = ContourSettings()
    s.fit_to(values, percentile=percentile)
    return s.vmin, s.vmax


class TestTheFieldDeclaresItsPercentile:
    def test_the_default_is_the_98th_percentile(self):
        assert ContourField("k", "K").fit_percentile == 0.98

    def test_a_program_gives_its_own(self):
        assert ContourField("k", "K", fit_percentile=1.0).fit_percentile == 1.0
        assert ContourField("k", "K", fit_percentile=1).fit_percentile == 1
        assert ContourField("k", "K", fit_percentile=0.5).fit_percentile == 0.5

    def test_a_wrong_percentile_is_refused_naming_the_field(self):
        for bad in (0, 0.0, -0.1, 1.01, 2, math.nan, math.inf, -math.inf,
                    "0.9", None, True, False):
            try:
                ContourField("sigma_1", "Stress", fit_percentile=bad)
            except ValueError as exc:
                text = str(exc)
                assert "sigma_1" in text, (bad, text)
                assert "(0, 1]" in text, (bad, text)
            else:
                raise AssertionError(f"{bad!r} was accepted")


class TestTheFitWithAPercentile:
    def test_the_index_of_the_percentile(self):
        values = [float(i) for i in range(100)]
        # round(0.98 * 99) = round(97.02) = 97
        assert _fit(values, 0.98) == (0.0, 97.0)
        assert _fit(values, 1.0) == (0.0, 99.0)

    def test_the_peak_is_left_out_at_098_and_kept_at_1(self):
        lo, hi = _fit(_PEAKED, 0.98)
        assert lo == 1.0 and abs(hi - 1.98) < 1e-12
        assert _fit(_PEAKED, 1.0) == (1.0, 50.0)

    def test_a_negative_peak_is_always_the_minimum(self):
        values = [-50.0] + [1.0 + i / 100 for i in range(100)]
        assert _fit(values, 0.98)[0] == -50.0
        assert _fit(values, 1.0)[0] == -50.0

    def test_values_that_are_not_finite_do_not_count(self):
        values = [1.0, 2.0, 3.0, math.nan, math.inf, -math.inf]
        assert _fit(values, 1.0) == (1.0, 3.0)

    def test_one_value_or_all_equal_open_the_same_range(self):
        # hi <= lo: hi = lo + max(|lo| * 0.1, 1.0)
        for p in (0.98, 1.0):
            assert _fit([3.0], p) == (3.0, 4.0)
            assert _fit([2.0] * 20, p) == (2.0, 3.0)
            assert _fit([20.0] * 5, p) == (20.0, 22.0)


# ======================================================================
# The dialog
# ======================================================================
#: Two automatic fields over the same values: one that trims (the default)
#: and one that keeps the whole range, as OGR FEM2D declares a stress.
_TRIM = ContourField("trim", "Trimmed")
_WHOLE = ContourField("whole", "Whole", fit_percentile=1.0)


def _app():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _dialog(field, fields=(_TRIM, _WHOLE), values=_PEAKED, language="en"):
    """A Contour Options dialog opened on ``field`` with ``values`` (which
    belong to that field), in ``language``, deleted afterwards."""
    import shiboken6
    from ogr_ui.dialogs.contour_options_dialog import ContourOptionsDialog
    from ogr_ui.i18n import current_language, set_language
    _app()
    before = current_language()
    try:
        set_language(language)
        d = ContourOptionsDialog(field.defaults(), fields, values, (), None)
        try:
            yield d
        finally:
            if shiboken6.isValid(d):
                shiboken6.delete(d)
    finally:
        set_language(before)


def _restore(d):
    from PySide6.QtWidgets import QDialogButtonBox
    box = d.findChild(QDialogButtonBox)
    box.button(QDialogButtonBox.RestoreDefaults).click()


def _pick(d, key):
    d.cbo_field.setCurrentIndex(d.cbo_field.findData(key))


class TestTheDialogFitsWithTheFieldsPercentile:
    def test_fit_to_results_and_what_the_dialog_returns(self):
        for field, top in ((_TRIM, 1.98), (_WHOLE, 50.0)):
            with _dialog(field) as d:
                d.chk_auto.setChecked(False)
                d.sp_max.setValue(7.0)
                d.btn_fit.click()
                assert abs(d.sp_max.value() - top) < 1e-9, field.key
                assert d.sp_min.value() == 1.0
                d._accept()
                assert abs(d.settings.vmax - top) < 1e-9, field.key
                assert d.settings.field == field.key

    def test_the_automatic_range_shows_the_fields_fit(self):
        for field, top in ((_TRIM, 1.98), (_WHOLE, 50.0)):
            with _dialog(field) as d:
                # the field starts automatic: shown as soon as it opens
                assert d.chk_auto.isChecked() is True
                assert abs(d.sp_max.value() - top) < 1e-9, field.key
                d.chk_auto.setChecked(False)
                d.sp_max.setValue(7.0)
                d.chk_auto.setChecked(True)
                assert abs(d.sp_max.value() - top) < 1e-9, field.key

    def test_restore_defaults_fits_with_the_fields_percentile(self):
        for field, top in ((_TRIM, 1.98), (_WHOLE, 50.0)):
            with _dialog(field) as d:
                d.chk_auto.setChecked(False)
                d.sp_max.setValue(7.0)
                _restore(d)
                assert abs(d.sp_max.value() - top) < 1e-9, field.key

    def test_there_and_back_between_fields(self):
        """The values are the opening field's, so they fit only back on
        it -- and with ITS percentile, not the one of the field passed
        through."""
        for field, other, top in ((_TRIM, _WHOLE, 1.98),
                                  (_WHOLE, _TRIM, 50.0)):
            with _dialog(field) as d:
                _pick(d, other.key)
                _pick(d, field.key)
                assert abs(d.sp_max.value() - top) < 1e-9, field.key


class TestNoPercentileIsVersion010:
    def test_the_ranges_of_010(self):
        # 0.1.0 fitted every field at 0.98: 0..99 gave 0 to 97
        # (round(0.98 * 99) = 97), with the button and automatically.
        plain = ContourField("plain", "Plain")
        values = [float(i) for i in range(100)]
        with _dialog(plain, fields=(plain,), values=values) as d:
            assert (d.sp_min.value(), d.sp_max.value()) == (0.0, 97.0)
            d.chk_auto.setChecked(False)
            d.sp_max.setValue(7.0)
            d.btn_fit.click()
            assert (d.sp_min.value(), d.sp_max.value()) == (0.0, 97.0)

    def test_settings_with_no_field_list(self):
        from ogr_ui.dialogs.contour_options_dialog import ContourOptionsDialog
        import shiboken6
        _app()
        d = ContourOptionsDialog(ContourSettings.automatic("x"), (),
                                 _PEAKED, (), None)
        try:
            assert abs(d.sp_max.value() - 1.98) < 1e-9
        finally:
            shiboken6.delete(d)


# ======================================================================
# The help of the automatic-range checkbox
# ======================================================================
_TRIMS_EN = ("Left on, the range follows the data as results change. The "
             "upper bound uses a percentile so a single extreme value "
             "cannot squash everything else into one band.")
_WHOLE_EN = ("Left on, the range follows the data as results change, from "
             "the smallest value to the largest.")
_TRIMS_ES = ("Activado, el rango sigue a los datos según cambian los "
             "resultados. El límite superior usa un percentil para que un "
             "único valor extremo no aplaste todo lo demás en una sola "
             "banda.")
_WHOLE_ES = ("Activado, el rango sigue a los datos según cambian los "
             "resultados, del menor valor al mayor.")
_ALMOST = ContourField("almost", "Almost", fit_percentile=0.9999)


class TestTheHelpSaysWhatTheFieldDoes:
    def test_in_english_and_in_spanish(self):
        for language, trims, whole in (("en", _TRIMS_EN, _WHOLE_EN),
                                       ("es", _TRIMS_ES, _WHOLE_ES)):
            fields = (_TRIM, _WHOLE, _ALMOST)
            for field, text in ((_TRIM, trims), (_ALMOST, trims),
                                (_WHOLE, whole)):
                with _dialog(field, fields=fields,
                             language=language) as d:
                    assert d.chk_auto.toolTip() == text, (language,
                                                          field.key)

    def test_it_follows_a_change_of_field_both_ways(self):
        for language, trims, whole in (("en", _TRIMS_EN, _WHOLE_EN),
                                       ("es", _TRIMS_ES, _WHOLE_ES)):
            with _dialog(_TRIM, language=language) as d:
                _pick(d, _WHOLE.key)
                assert d.chk_auto.toolTip() == whole, language
                _pick(d, _TRIM.key)
                assert d.chk_auto.toolTip() == trims, language

    def test_no_percentile_is_the_help_of_010(self):
        plain = ContourField("plain", "Plain")
        with _dialog(plain, fields=(plain,)) as d:
            assert d.chk_auto.toolTip() == _TRIMS_EN

    def test_the_dialog_fits_1366_by_728_in_spanish_with_each_field(self):
        for field in (_TRIM, _WHOLE):
            with _dialog(field, language="es") as d:
                for key in (_TRIM.key, _WHOLE.key):
                    _pick(d, key)
                    hint = d.sizeHint()
                    assert hint.width() <= 1366, (key, hint)
                    assert hint.height() <= 728, (key, hint)
