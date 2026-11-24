# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — the version is said once, in two places that agree, and a release
has its changelog.

The rule of OGR Core (its ``AGENTS.md``, rule 9), the same here because the
programs pin this package by tag as they pin the core: the number is in
``pyproject.toml`` and in ``ogr_ui/__init__.py``; it is ``X.Y.Z`` in the
commit that is tagged and ``X.Y.Z.dev0`` between two tags, so that a changed
and untagged tree never answers for the tagged one. OGR Slip2D says its
version in seven places and keeps a test for the same reason: a list in a
document is only worth the attention of whoever reads it.

The invariants:

* the two numbers are equal;
* the number is a release (``X.Y.Z``) or the development of one
  (``X.Y.Z.devN``), nothing else;
* a release has ``docs/changelog/CHANGELOG_vX.Y.Z.md``, and a development
  version has the changelog of the release before it;
* the core the tests run on is pinned in the ``test`` extra, as a tag, and
  is not a dependency of the package.
"""
from __future__ import annotations

import re
import tomllib
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent


def _pyproject() -> dict:
    return tomllib.loads((_ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def _declared() -> str:
    return _pyproject()["project"]["version"]


def _package() -> str:
    text = (_ROOT / "ogr_ui" / "__init__.py").read_text(encoding="utf-8")
    return re.search(r'^__version__\s*=\s*"([^"]+)"', text, re.M).group(1)


class TestTheVersion:
    def test_the_two_places_agree(self):
        assert _declared() == _package(), (_declared(), _package())

    def test_it_is_a_release_or_the_development_of_one(self):
        assert re.fullmatch(r"\d+\.\d+\.\d+(\.dev\d+)?", _declared()), _declared()

    def test_a_release_has_its_changelog(self):
        v = _declared()
        base = v.split(".dev")[0]
        folder = _ROOT / "docs" / "changelog"
        if ".dev" not in v:
            assert (folder / f"CHANGELOG_v{v}.md").is_file(), v
        else:
            # the release this one leads to is later than every release
            # that has a changelog: a .dev of an old number would answer
            # for a tag that already exists
            def key(s):
                return tuple(int(x) for x in s.split("."))
            released = [p.stem[len("CHANGELOG_v"):]
                        for p in folder.glob("CHANGELOG_v*.md")]
            assert released, "no changelog of a previous release"
            assert all(key(base) > key(r) for r in released), (base, released)


class TestTheCoreIsForTheTestsOnly:
    def test_it_is_pinned_in_the_test_extra_to_a_tag(self):
        extras = _pyproject()["project"]["optional-dependencies"]["test"]
        pins = [r for r in extras if r.lower().startswith("ogr-core")]
        assert len(pins) == 1, extras
        assert re.search(r"@\s*git\+https://github\.com/samuelsl27/OGR-Core@v\d+\.\d+\.\d+$",
                         pins[0]), pins[0]

    def test_it_is_not_a_dependency_of_the_package(self):
        deps = _pyproject()["project"]["dependencies"]
        assert not [d for d in deps if re.match(r"\s*ogr[-_.]", d, re.I)], deps

    def test_the_runner_reads_the_same_pin(self):
        import _runner
        extras = _pyproject()["project"]["optional-dependencies"]["test"]
        tag = re.search(r"@v(\d+\.\d+\.\d+)$", extras[0]).group(1)
        assert _runner.pinned() == {"ogr_core": tag}
