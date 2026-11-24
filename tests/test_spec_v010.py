# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — the specification-driven layout of the repository holds together.

The suite works by specifications (the hello-sdd method, as OGR FEM2D and
OGR Data): a constitution in ``spec/constitution/`` and one folder per
change in ``spec/features/NNN-name/`` with ``spec.md``, ``plan.md`` and
``tasks.md``. Nothing checks a document by itself, and a layout that only a
document describes drifts: a spec marked done with a task left open, a
requirement that no task and no test mention, a constitution file that
``AGENTS.md`` no longer points to.

The invariants:

* the constitution has its files, and ``AGENTS.md`` links each of them;
* the design references number their principles D-1 to D-14, each once;
* every feature folder is ``NNN-kebab-name`` with the three files, and the
  numbers do not repeat;
* a spec whose state says «hecha» has every task ticked, and every one of
  its requirements (``RF-n``) appears in its ``tasks.md`` and in the table
  of its «Validación» section;
* the roadmap lists every spec that is done.

Standard library only.
"""
from __future__ import annotations

import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SPEC = _ROOT / "spec"
_CONSTITUTION = ("mission.md", "principles.md", "tech-stack.md", "roadmap.md",
                 "referencias-de-diseno.md")
_FEATURE = re.compile(r"^(\d{3})-[a-z0-9]+(?:-[a-z0-9]+)*$")
_RF = re.compile(r"\bRF-(\d+)\b")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _features() -> list:
    return sorted(p for p in (_SPEC / "features").iterdir() if p.is_dir())


def _done(spec_md: str) -> bool:
    first = next((ln for ln in spec_md.splitlines() if ln.startswith("> Estado")), "")
    return "hecha" in first.lower()


def _rf_range(token: str) -> set:
    """``RF-3–RF-7`` (a range written in a task) as {3, ..., 7}."""
    m = re.fullmatch(r"RF-(\d+)\s*[–-]\s*RF-(\d+)", token)
    if m:
        return set(range(int(m.group(1)), int(m.group(2)) + 1))
    return {int(n) for n in _RF.findall(token)}


def _mentioned(text: str) -> set:
    found = set()
    for m in re.finditer(r"RF-\d+(?:\s*[–-]\s*RF-\d+)?", text):
        found |= _rf_range(m.group(0))
    return found


class TestTheConstitution:
    def test_its_files_are_there_and_agents_links_them(self):
        agents = _text(_ROOT / "AGENTS.md")
        for name in _CONSTITUTION:
            assert (_SPEC / "constitution" / name).is_file(), name
        for name in ("principles.md", "referencias-de-diseno.md"):
            assert f"spec/constitution/{name}" in agents, name

    def test_the_design_principles_are_numbered_once_each(self):
        text = _text(_SPEC / "constitution" / "referencias-de-diseno.md")
        heads = re.findall(r"^### D-(\d+)\.", text, re.M)
        assert [int(n) for n in heads] == list(range(1, 15)), heads

    def test_the_design_references_cite_the_eight_sources(self):
        text = _text(_SPEC / "constitution" / "referencias-de-diseno.md")
        for url in ("lawsofux.com", "fluent2.microsoft.design",
                    "checklist.design", "github.com/Autodesk/hig",
                    "humanebydesign.com", "growth.design/psychology",
                    "goodui.org", "deceptive.design"):
            assert url in text, url


class TestTheFeatures:
    def test_every_folder_is_numbered_and_has_its_three_files(self):
        numbers = []
        for folder in _features():
            m = _FEATURE.match(folder.name)
            assert m, folder.name
            numbers.append(m.group(1))
            for name in ("spec.md", "plan.md", "tasks.md"):
                assert (folder / name).is_file(), (folder.name, name)
        assert len(numbers) == len(set(numbers)), numbers
        assert "000" in numbers, "the template is missing"

    def test_a_done_spec_has_every_task_ticked(self):
        for folder in _features():
            if folder.name.startswith("000"):
                continue
            if _done(_text(folder / "spec.md")):
                tasks = _text(folder / "tasks.md")
                assert "- [ ]" not in tasks, folder.name
                assert "- [x]" in tasks, folder.name

    def test_every_requirement_of_a_done_spec_is_tasked_and_validated(self):
        for folder in _features():
            if folder.name.startswith("000"):
                continue
            spec = _text(folder / "spec.md")
            if not _done(spec):
                continue
            declared = {int(n) for n in re.findall(r"\*\*RF-(\d+)\*\*", spec)}
            assert declared, folder.name
            tasked = _mentioned(_text(folder / "tasks.md"))
            assert declared <= tasked, (folder.name, sorted(declared - tasked))
            assert "## Validación" in spec, folder.name
            validated = _mentioned(spec.split("## Validación", 1)[1])
            assert declared <= validated, (folder.name, sorted(declared - validated))

    def test_the_roadmap_lists_every_done_spec(self):
        roadmap = _text(_SPEC / "constitution" / "roadmap.md")
        for folder in _features():
            if folder.name.startswith("000"):
                continue
            if _done(_text(folder / "spec.md")):
                assert f"features/{folder.name}/" in roadmap, folder.name


class TestTheReadingOfRanges:
    def test_a_range_and_a_list(self):
        assert _mentioned("— RF-3–RF-5, RF-9") == {3, 4, 5, 9}
        assert _mentioned("RF-1, RF-2") == {1, 2}
        assert _mentioned("nothing here") == set()
