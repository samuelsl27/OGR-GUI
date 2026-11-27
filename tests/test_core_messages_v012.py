# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI 0.1.2 — the Spanish of the coded messages of the core (spec 003).

The core does not translate: a message leaves ``ogr_core`` with a code,
an English template and its values, and ``ogr_core.messages.render`` says
it with the program's ``tr()``. OGR FEM2D asked (2026-11-25) for the
Spanish of ``ogr_core.api``; the owner widened it to every coded
catalogue of the core. It lives in :mod:`ogr_ui.i18n.core_es`, and
``tr()`` has it with nothing for the program to do.

The core enters HERE only, from the ``[test]`` extra (v0.2.12); the
package itself never imports it (``test_layering_v010``).

The invariants:

* **every template is translated**: the English and the singular of every
  catalogue found in the core, and a missing one is named with its
  catalogue and its code (RF-1, RF-5). The catalogues are found by walking
  the core, so a new one cannot go unchecked when the tag moves; the
  twenty of v0.2.12 are asserted, so a broken walk cannot pass in silence;
* **with nothing to do**: ``tr()`` in Spanish has them, and ``render`` with
  ``translate=tr`` says an error of ``ogr_core.api`` in Spanish (RF-2);
* **the words are Slip2D's**: every entry of the frozen copy of Slip2D's
  dictionary at ``67faf4f`` is the same here, but those of RF-8 (none, at
  this version) and RF-9, which differ and are named in the changelog
  (RF-3, RF-8, RF-9);
* **the fields are the template's**: name, conversion and format of every
  field, as a multiset (RF-4);
* **a template with no words has no entry** (RF-6), and **one of a newer
  core stays in English** (RF-7).

Every test puts back the language it set (rule 5).

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import collections
import contextlib
import importlib
import json
import pkgutil
import re
import string
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

#: The coded catalogues of ``ogr_core`` v0.2.12, as the walk names them
#: (the shortest module that holds each one).
CATALOGUES_0212 = frozenset({
    ("ogr_core.api", "API_MESSAGES"),
    ("ogr_core.messages", "CORE_MESSAGES"),
    ("ogr_core.messages", "NOTE_FRAMES"),
    ("ogr_core.dxf.messages", "MESSAGES"),
    ("ogr_core.dxf.messages", "EXPORT_MESSAGES"),
    ("ogr_core.fem.messages", "SEEPAGE_NOTES"),
    ("ogr_core.fem.messages", "REFINE_MESSAGES"),
    ("ogr_core.file_messages", "FILE_MESSAGES"),
    ("ogr_core.geometry.messages", "GEOMETRY_MESSAGES"),
    ("ogr_core.loads.messages", "SEISMIC_NOTES"),
    ("ogr_core.materials.messages", "CALCULATOR_NOTES"),
    ("ogr_core.materials.messages", "FACTORING_NOTES"),
    ("ogr_core.project.design_messages", "DESIGN_NOTES"),
    ("ogr_core.project.messages", "RULES"),
    ("ogr_core.project.messages", "REFUSALS"),
    ("ogr_core.project.messages", "STRENGTH_REFUSALS"),
    ("ogr_core.project.messages", "IMPORT_NOTES"),
    ("ogr_core.project.reported", "REPORTED_NOTES"),
    ("ogr_core.project.step_names", "STEP_NAMES"),
    ("ogr_core.statistics.messages", "SWEEP_NOTES"),
})

#: RF-8: Slip2D's translations with limit-equilibrium words where the
#: template is general, replaced here by neutral ones. The search of the
#: plan (dovela, talud, superficie de deslizamiento, factor de seguridad,
#: FS, método, rotura against their English) and the reading by hand of
#: every Spanish entry with one of those words found none at 0.1.2: each
#: such word is in its English template too.
RF8: dict = {}

#: RF-9: Slip2D's translations that do not keep the fields of their
#: template -- «{name}» where the template says {name!r} -- taken with
#: Slip2D's words and the template's fields (the owner, 2026-11-27).
RF9: dict = {
    "{name!r} used a water surface of the other project; assign one of "
    "this model to it.": "import.water_dropped",
    "{name!r} lost its anisotropic surface, which belonged to the other "
    "project.": "import.anisotropic_dropped",
    "{name!r}: {who} now takes the strength of {here!r}, the material of "
    "that name in this model.": "import.link_renamed",
    "{name!r}: {who} linked a material this model cannot link; it keeps "
    "the strength it had, unlinked.": "import.link_dropped",
}

#: The frozen copy of Slip2D's Spanish of the core's templates at
#: ``67faf4f`` (v0.1.492, on the core v0.2.12): the evidence of RF-3, not a
#: dictionary anything uses. Slip2D's repository is not in the CI.
_SLIP2D = _ROOT / "tests" / "data" / "slip2d_core_es_67faf4f.json"

#: Modules of the core that do not import without an optional dependency
#: of its own; checked to hold no catalogue, so skipping them hides none.
_OPTIONAL = frozenset({"ogr_core.statistics.probabilistic",
                       "ogr_core.statistics.sensitivity"})


# ======================================================================
# The catalogues, the templates and their fields
# ======================================================================
def _catalogues():
    """``{(module, name): catalogue}`` of every dictionary of
    ``MessageSpec`` in ``ogr_core``, each catalogue once, and the modules
    that did not import."""
    import ogr_core
    from ogr_core.messages import MessageSpec
    held, failed = {}, []
    for info in pkgutil.walk_packages(ogr_core.__path__, "ogr_core."):
        if ".testing" in info.name:
            continue
        try:
            module = importlib.import_module(info.name)
        except ImportError:
            failed.append(info.name)
            continue
        for name, value in vars(module).items():
            if (isinstance(value, dict) and value
                    and all(isinstance(v, MessageSpec)
                            for v in value.values())):
                held.setdefault(id(value), (value, []))[1].append(
                    (info.name, name))
    found = {}
    for value, names in held.values():
        found[min(names, key=lambda n: (len(n[0]), n))] = value
    return found, failed


def _templates(found=None):
    """``[(module, catalogue, code, which, template)]`` of the core's
    catalogues (or of ``found``), each template as often as it appears."""
    if found is None:
        found, _ = _catalogues()
    out = []
    for (module, name), catalogue in sorted(found.items()):
        for code, spec in catalogue.items():
            out.append((module, name, code, "english", spec.english))
            if spec.one:
                out.append((module, name, code, "one", spec.one))
    return out


def wordless(template: str) -> bool:
    """True when nothing is left to translate once the fields are out:
    no letter outside ``{...}`` (RF-6)."""
    literal = "".join(text for text, *_ in string.Formatter().parse(template))
    return re.search(r"[^\W\d_]", literal) is None


def fields(template: str) -> collections.Counter:
    """The fields of ``template`` as a multiset of (name, conversion,
    format); doubled braces are literal text (RF-4)."""
    return collections.Counter(
        (name, conversion, spec)
        for _, name, spec, conversion in string.Formatter().parse(template)
        if name is not None)


def missing(table: dict, found=None) -> list:
    """The templates with words and no entry in ``table``, each named by
    its catalogue and its code (RF-5)."""
    return [f"{module}.{name} {code} ({which}): {template!r}"
            for module, name, code, which, template in _templates(found)
            if not wordless(template) and template not in table]


def _core_es():
    from ogr_ui.i18n.core_es import CORE_ES
    return CORE_ES


@contextlib.contextmanager
def _language(code):
    from ogr_ui.i18n import current_language, set_language
    before = current_language()
    set_language(code)
    try:
        yield
    finally:
        set_language(before)


# ======================================================================
class TestTheCataloguesAreFound:
    def test_the_twenty_of_0212(self):
        import ogr_core
        assert ogr_core.__version__ == "0.2.12", ogr_core.__version__
        found, _ = _catalogues()
        assert set(found) == CATALOGUES_0212, (
            sorted(set(found) - CATALOGUES_0212),
            sorted(CATALOGUES_0212 - set(found)))

    def test_what_did_not_import_holds_no_catalogue(self):
        import ogr_core
        _, failed = _catalogues()
        assert set(failed) <= _OPTIONAL, failed
        base = Path(ogr_core.__file__).parent
        for name in failed:
            path = base.joinpath(*name.split(".")[1:]).with_suffix(".py")
            assert "MessageSpec" not in path.read_text(encoding="utf-8"), name


class TestEveryTemplateIsTranslated:
    def test_none_is_missing(self):
        gone = missing(_core_es())
        assert gone == [], f"{len(gone)} without Spanish: {gone[:20]}"

    def test_a_missing_one_is_named_with_its_catalogue_and_code(self):
        found = missing({})
        assert ("ogr_core.api.API_MESSAGES api.model.none_open (english): "
                "'No model is open.'") in found

    def test_the_singular_is_checked_too(self):
        """No catalogue of v0.2.12 has a singular form (Slip2D's own
        messages do); one made here shows that it would be checked."""
        from ogr_core.messages import MessageSpec
        made = {("x.made", "NOTES"): {"x.n": MessageSpec(
            "x.n", "{n} values were left out.", count="n",
            one="One value was left out.")}}
        assert missing({"{n} values were left out.": "x"}, made) == [
            "x.made.NOTES x.n (one): 'One value was left out.'"]
        assert missing({"{n} values were left out.": "x",
                        "One value was left out.": "y"}, made) == []

    def test_every_entry_is_a_template_of_the_core(self):
        """No entry left over from a template the core no longer has."""
        templates = {t for *_, t in _templates()}
        extra = sorted(set(_core_es()) - templates)
        assert extra == [], extra

    def test_the_spanish_is_not_the_english(self):
        from ogr_ui.i18n.core_es import CORE_ES
        from test_i18n_v010 import IDENTICAL
        same = sorted(k for k, v in CORE_ES.items()
                      if v == k and k not in IDENTICAL)
        assert same == [], same


class TestNothingForTheProgramToDo:
    def test_tr_has_them(self):
        from ogr_ui.i18n import tr
        with _language("es"):
            assert tr("No model is open.") == "No hay ningún modelo abierto."
            assert tr("segments {k} and {j} cross or overlap") == (
                "los segmentos {k} y {j} se cruzan o se solapan")
        with _language("en"):
            assert tr("No model is open.") == "No model is open."

    def test_render_says_an_error_of_the_api_in_spanish(self):
        from ogr_core.api import API_MESSAGES
        from ogr_core.messages import render
        from ogr_ui.i18n import tr
        args = {"model": "p1", "what": "una lectura", "since": 3.4}
        with _language("es"):
            text = render(API_MESSAGES, "api.model.busy", args, "",
                          translate=tr)
        assert text == "El modelo p1 está ocupado con una lectura (3 s)."

    def test_no_key_is_both_a_piece_and_a_template(self):
        """The two tables of the package do not overlap, so neither
        changes the other when ``tr()`` starts with both."""
        from ogr_ui.i18n.es import ES
        assert sorted(set(ES) & set(_core_es())) == []

    def test_core_es_imports_nothing(self):
        import ast
        import ogr_ui.i18n.core_es as module
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        imported = [n for n in ast.walk(tree)
                    if isinstance(n, (ast.Import, ast.ImportFrom))
                    and not (isinstance(n, ast.ImportFrom)
                             and n.module == "__future__")]
        assert imported == []

    def test_the_package_hands_them_to_a_program(self):
        from ogr_ui.i18n import package_translations
        table = package_translations("es")
        assert table["No model is open."] == "No hay ningún modelo abierto."


class TestTheWordsAreSlip2Ds:
    def test_the_frozen_copy(self):
        slip2d = json.loads(_SLIP2D.read_text(encoding="utf-8"))
        assert len(slip2d) == 237
        es = _core_es()
        differ = sorted(k for k, v in slip2d.items()
                        if es.get(k) != v and k not in RF8 and k not in RF9)
        assert differ == [], differ

    def test_those_that_differ_do_and_are_in_the_changelog(self):
        slip2d = json.loads(_SLIP2D.read_text(encoding="utf-8"))
        es = _core_es()
        notes = [p for p in (_ROOT / "docs" / "changelog").glob("*0.1.2.md")]
        assert len(notes) == 1, notes
        text = notes[0].read_text(encoding="utf-8")
        for key, code in {**RF8, **RF9}.items():
            assert key in slip2d, code
            assert es[key] != slip2d[key], code
            assert f"`{code}`" in text, code

    def test_rf9_keeps_slip2ds_words(self):
        """Only the quotes of the field change."""
        slip2d = json.loads(_SLIP2D.read_text(encoding="utf-8"))
        es = _core_es()
        for key in RF9:
            ours = re.sub(r"\{(\w+)!r\}", r"«{\1}»", es[key])
            assert ours == slip2d[key], key
            assert fields(es[key]) == fields(key), key


class TestTheFieldsAreTheTemplates:
    def test_every_translation(self):
        es = _core_es()
        wrong = [code for _, _, code, _, t in _templates()
                 if t in es and fields(es[t]) != fields(t)]
        assert wrong == [], wrong

    def test_the_comparison_sees_a_bad_one(self):
        good = "Model {model} is busy ({since:.0f} s)."
        assert fields(good) == fields("{model} ocupado ({since:.0f} s).")
        assert fields(good) != fields("{model} ocupado ({since} s).")
        assert fields(good) != fields("ocupado ({since:.0f} s).")
        assert fields(good) != fields("{model} {model} ({since:.0f} s).")
        assert fields("{name!r} lost") != fields("«{name}» perdido")
        assert fields("A request is {{'id', 'op'}}.") == collections.Counter()


class TestAWordlessTemplate:
    def test_has_no_entry(self):
        es = _core_es()
        for template in ("{first}; {second}", "{type}: {text}",
                         "{method_id}: {note}", "{name} #{n}"):
            assert wordless(template), template
            assert template not in es, template

    def test_one_word_is_enough_to_translate(self):
        assert not wordless("pid {pid} ({title})")
        assert not wordless("{where} cannot be null.")
        assert not wordless("A request is {{'id'}}.")


class TestANewerCoreStaysInEnglish:
    def test_an_untranslated_template(self):
        from ogr_core.messages import MessageSpec, render
        from ogr_ui.i18n import tr
        catalogue = {"x.new": MessageSpec(
            "x.new", "A template of a newer core, with {n} values.")}
        with _language("es"):
            text = render(catalogue, "x.new", {"n": 3}, "", translate=tr)
        assert text == "A template of a newer core, with 3 values."
