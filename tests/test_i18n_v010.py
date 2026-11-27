# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — ``tr()`` switches language and tells its listeners, a program's
dictionary is added knowingly, and rule 2 holds for this package: every
visible text of ``ogr_ui`` goes through ``tr()`` and has its Spanish.

WHAT INVARIANT THIS PROTECTS, ported from OGR Slip2D (v0.1.486):

* the mechanism parts of ``tests/test_i18n_coverage_v141.py`` (v0.1.41;
  the language put back by a context manager since v0.1.231): English is
  the reference, an unknown key returns itself, switching changes the text,
  the available and current languages are reported. Its regex budgets
  (``_UNWRAPPED_BUDGET``, D300 and D103) are superseded by the AST census
  below, as they were in Slip2D; its checks of Slip2D's own terms and
  dialogs stay there;
* its rule 2 (every wrapped key has Spanish, no translation left identical
  outside a short allow-list), and the census of
  ``tests/test_gui_spanish_v1318.py`` (v0.1.318, D300; the rules of
  v0.1.432, D399, v0.1.433, D411 and v0.1.435, D413), both now functions
  of :mod:`ogr_ui.testing.texts`, applied to THIS package: the texts
  outside ``tr()`` are exactly :data:`EXCEPTIONS` (``BUDGET`` 0 after them),
  none of the exceptions is a ghost, and no field of a translated text is
  filled with English.

What OGR GUI 0.1.0 changed, tested here: the dictionary of this package is
``ogr_ui.i18n.es`` and a program adds its own with ``add_translations``,
which returns the keys whose translation it changed;
``remove_language_listener`` undoes ``on_language_changed``; and
``package_translations`` hands back a copy of what this package ships.

Every test puts back the language, the listeners and the dictionaries it
touched (rule 5).
"""
from __future__ import annotations

import contextlib
from pathlib import Path

import pytest

_PACKAGE = Path(__file__).resolve().parent.parent / "ogr_ui"
#: The dictionary, and the checks of the rules themselves (their sources
#: are sample texts, not interface).
_SKIP = ("i18n/", "testing/")

#: The texts outside ``tr()`` that are not to be translated, with the
#: reason: Slip2D's own exceptions for these same files
#: (tests/test_gui_spanish_v1318.py, v0.1.319).
EXCEPTIONS: dict = {
    ("widgets/legend.py", "X: 0.000   Y: 0.000"):
        "notation: the coordinates of the pointer",
    ("widgets/legend.py", "X: {}   Y: {}"):
        "notation: the coordinates of the pointer",
    ("widgets/status_bar.py", "X: {}   Y: {}"):
        "notation: the coordinates of the pointer",
    ("widgets/status_bar.py", "x, y"):
        "notation: the format of the coordinates to type",
}
#: How many may be left after the exceptions. Lowering it is the point;
#: raising it needs a reason in a changelog. 0 since this package's first
#: version, as Slip2D's at v0.1.320.
BUDGET = 0

#: The Spanish translations that are the English text, each a decision
#: (Slip2D's allow-list in tests/test_i18n_coverage_v141.py, these entries).
IDENTICAL: dict = {
    "Horizontal:": "a cognate: the same word in Spanish",
    "Vertical:": "a cognate: the same word in Spanish",
    "SNAP": "a status-bar acronym kept as it is, so the two languages "
            "read the same width",
    "OSNAP": "a status-bar acronym kept as it is, so the two languages "
             "read the same width",
    "Snap": "the name of the status-bar toggle SNAP, kept with it",
    "X: 0.000   Y: 0.000": "a pure format string: the coordinates",
    # 0.1.2 (spec 003), templates of ogr_core.api
    "error": "api.error: the same word in Spanish",
    "pid {pid} ({title})": "api.bridge.listing.item: 'pid', the process "
                           "identifier, is written so in Spanish too",
}


@contextlib.contextmanager
def _language(code):
    """The language set for a block, and the one before it put back on the
    way out, whatever happens inside (Slip2D v0.1.231)."""
    from ogr_ui.i18n import current_language, set_language
    before = current_language()
    set_language(code)
    try:
        yield
    finally:
        set_language(before)


@contextlib.contextmanager
def _dictionaries():
    """The tables of ``ogr_ui.i18n`` as they were, put back on the way out:
    every language, every entry."""
    import ogr_ui.i18n as i18n
    saved = {lang: dict(table) for lang, table in i18n._DICTS.items()}
    try:
        yield i18n
    finally:
        for lang in list(i18n._DICTS):
            if lang not in saved:
                del i18n._DICTS[lang]
        for lang, table in saved.items():
            i18n._DICTS[lang].clear()
            i18n._DICTS[lang].update(table)


# ======================================================================
class TestTheMechanism:

    def test_english_is_the_reference(self):
        from ogr_ui.i18n import tr
        with _language("en"):
            assert tr("Cancel") == "Cancel"
            assert tr("Computing...") == "Computing..."

    def test_switching_changes_the_text(self):
        from ogr_ui.i18n import set_language, tr
        with _language("es"):
            assert tr("Cancel") == "Cancelar"
            set_language("en")
            assert tr("Cancel") == "Cancel"

    def test_unknown_key_returns_itself(self):
        from ogr_ui.i18n import tr
        with _language("es"):
            assert tr("a key that does not exist") == \
                "a key that does not exist"

    def test_available_and_current_languages(self):
        from ogr_ui.i18n import (available_languages, current_language,
                                 set_language)
        langs = available_languages()
        assert langs[:2] == ["en", "es"], langs
        with _language("es"):
            assert current_language() == "es"
            set_language("en")
            assert current_language() == "en"

    def test_an_unknown_language_is_refused(self):
        from ogr_ui.i18n import current_language, set_language
        heard = []
        with _listening(heard.append):
            before = current_language()
            with pytest.raises(KeyError):
                set_language("tlh")
            assert current_language() == before
            assert heard == [], "a refused language was announced"


@contextlib.contextmanager
def _listening(cb):
    from ogr_ui.i18n import on_language_changed, remove_language_listener
    on_language_changed(cb)
    try:
        yield
    finally:
        remove_language_listener(cb)


class TestTheListeners:

    def test_a_listener_hears_every_switch(self):
        heard = []
        from ogr_ui.i18n import set_language
        with _language("en"), _listening(heard.append):
            set_language("es")
            set_language("en")
        assert heard == ["es", "en"]

    def test_a_removed_listener_hears_nothing(self):
        import ogr_ui.i18n as i18n
        heard = []
        before = list(i18n._LISTENERS)
        with _language("en"):
            i18n.on_language_changed(heard.append)
            i18n.remove_language_listener(heard.append)
            i18n.set_language("es")
        assert heard == []
        assert i18n._LISTENERS == before

    def test_removing_one_never_added_is_a_no_op(self):
        import ogr_ui.i18n as i18n
        before = list(i18n._LISTENERS)
        i18n.remove_language_listener(lambda code: None)
        assert i18n._LISTENERS == before

    def test_a_listener_that_fails_stops_neither_the_switch_nor_the_rest(self):
        from ogr_ui.i18n import current_language, set_language
        heard = []

        def broken(code):
            raise RuntimeError("a closed window")
        with _language("en"), _listening(broken), _listening(heard.append):
            set_language("es")
            assert current_language() == "es"
            assert heard == ["es"]

    def test_a_listener_may_remove_itself(self):
        """``set_language`` calls a copy of the list: a window that closes
        on the switch does not make the next listener be skipped."""
        import ogr_ui.i18n as i18n
        heard = []

        def once(code):
            heard.append(("once", code))
            i18n.remove_language_listener(once)
        with _language("en"), _listening(once), \
                _listening(lambda c: heard.append(("next", c))):
            i18n.set_language("es")
        assert heard[:2] == [("once", "es"), ("next", "es")], heard


class TestAProgramsDictionary:

    def test_new_keys_change_nothing_of_the_package(self):
        from ogr_ui.i18n import tr
        with _dictionaries() as i18n, _language("es"):
            changed = i18n.add_translations("es", {"Boundaries": "Contornos"})
            assert changed == []
            assert tr("Boundaries") == "Contornos"

    def test_the_same_translation_again_is_no_change(self):
        with _dictionaries() as i18n:
            assert i18n.add_translations("es", {"Cancel": "Cancelar"}) == []

    def test_a_different_translation_is_named(self):
        from ogr_ui.i18n import tr
        from ogr_ui.i18n.es import ES
        with _dictionaries() as i18n, _language("es"):
            changed = i18n.add_translations(
                "es", {"Cancel": "Anular", "Theme": "Tema",
                       "Computing...": "Computando...", "New": "Nuevo"})
            assert changed == ["Cancel", "Computing..."]
            assert tr("Cancel") == "Anular"
            # the package's own dictionary is not touched
            assert ES["Cancel"] == "Cancelar"
            assert i18n.package_translations("es")["Cancel"] == "Cancelar"
        with _language("es"):
            assert tr("Cancel") == "Cancelar", "the test did not put it back"

    def test_a_new_language(self):
        from ogr_ui.i18n import available_languages, tr
        with _dictionaries() as i18n:
            assert i18n.add_translations("fr", {"Cancel": "Annuler"}) == []
            assert "fr" in available_languages()
            with _language("fr"):
                assert tr("Cancel") == "Annuler"
                assert tr("Theme") == "Theme", "falls back to the key"
        assert "fr" not in available_languages()

    def test_package_translations_is_a_copy(self):
        from ogr_ui.i18n import package_translations, tr
        from ogr_ui.i18n.core_es import CORE_ES
        from ogr_ui.i18n.es import ES
        table = package_translations("es")
        # 0.1.2 (spec 003): the pieces' texts and the core's messages
        assert table == {**CORE_ES, **ES}
        assert table is not ES and table is not CORE_ES
        table["Cancel"] = "something else"
        with _language("es"):
            assert tr("Cancel") == "Cancelar"
        assert package_translations("en") == {}
        assert package_translations("fr") == {}

    def test_the_active_table_starts_as_the_package(self):
        import ogr_ui.i18n as i18n
        from ogr_ui.i18n.es import ES
        assert i18n._DICTS["es"] is not ES
        assert i18n._DICTS["en"] == {}


# ======================================================================
class TestRuleTwoInThisPackage:
    """Every key ``ogr_ui`` wraps in ``tr()`` has Spanish, none is left
    identical but the allow-list (test_i18n_coverage_v141)."""

    def test_the_scan_reads_the_package(self):
        from ogr_ui.testing import texts
        keys = texts.wrapped_keys(_PACKAGE, skip=_SKIP)
        # one key from each kind of module: a dialog, a widget, the tasks
        for key in ("Computing...", "Preferences", "Saving the results file...",
                    "Contour Options"):
            assert key in keys, key

    def test_every_wrapped_key_has_spanish(self):
        from ogr_ui.i18n import package_translations
        from ogr_ui.testing import texts
        missing = texts.missing_translations(
            texts.wrapped_keys(_PACKAGE, skip=_SKIP),
            package_translations("es"))
        assert not missing, f"{len(missing)} keys without Spanish: {missing}"

    def test_no_lazy_identity_translations(self):
        from ogr_ui.i18n import package_translations
        from ogr_ui.testing import texts
        same = texts.identical_translations(package_translations("es"),
                                            IDENTICAL)
        assert same == [], same

    def test_the_allow_list_is_not_slack(self):
        """Each allowed entry is in the dictionary, still identical, and
        has its reason."""
        from ogr_ui.i18n import package_translations
        es = package_translations("es")
        for key, why in IDENTICAL.items():
            assert es.get(key) == key, key
            assert why.strip(), key


class TestNoInterfaceTextSkipsTr:
    """The census of test_gui_spanish_v1318, over ``ogr_ui``."""

    def test_the_budget_is_exact(self):
        from ogr_ui.testing import texts
        left = texts.counted(_PACKAGE, EXCEPTIONS, skip=_SKIP)
        assert len(left) == BUDGET, (len(left), left[:40])

    def test_no_exception_is_a_ghost(self):
        from ogr_ui.testing import texts
        assert texts.ghost_exceptions(_PACKAGE, EXCEPTIONS, skip=_SKIP) == []

    def test_no_field_is_filled_with_english(self):
        from ogr_ui.testing import texts
        found = texts.field_census(_PACKAGE, skip=_SKIP)
        assert not found, found
