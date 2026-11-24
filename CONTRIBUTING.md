# Contributing to OGR GUI

Thanks for wanting to help. *OpenGeoRock* (or *OGR Suite*) is the umbrella over the suite's
programs; **OGR GUI** is the set of interface pieces they share, and it is what this repository
contains. The package is imported as `ogr_ui`.

Licence: **AGPL-3.0-or-later**. Contributions are accepted under the terms in [`CLA.md`](CLA.md),
the same agreement as the rest of the suite. Read it before your first pull request.

---

## Getting set up

```bash
git clone https://github.com/samuelsl27/OGR-GUI.git
cd OGR-GUI
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test]"
QT_QPA_PLATFORM=offscreen python tests/_runner.py
```

The `[test]` extra brings OGR Core at the tag it pins: the suite's test runner lives there. The
package itself does not import it.

The runner exits non-zero if anything fails, which is what CI checks (Linux, Windows and macOS). A
pattern that matches nothing **exits 2**, and a filtered run prints a `FILTERED RUN` warning around
its totals: before opening a pull request, run the suite with no arguments.

A test file that leaves something changed in the process (the language, the theme, the style
sheet, an attribute of a module) **fails the run even when its tests pass**: the runner names it
with `✗ [LEAK]`. Put it back in the test.

## What a change must satisfy

The rules are in [`AGENTS.md`](AGENTS.md) (in Spanish), which is the single source and applies
equally to people and to AI agents. In short: every visible text goes through `tr()` and has its
Spanish; nothing here imports the core or a program; every source file carries the licence header;
tests leak no state; anomalies are reported before they are corrected; and no setting may do
nothing.

## Commits and branches

- Branch from `main` as `dev/short-description`.
- Sign off your commits: `git commit -s -m "..."` (Developer Certificate of Origin).
- Write commit subjects that say what changed and why.

## Versioning

`0.MINOR.PATCH` while pre-1.0, in its own series. Each release bumps the version in
`pyproject.toml` and `ogr_ui/__init__.py` (a test fails if they disagree), is tagged `vX.Y.Z`, and
adds a changelog entry recording **what was found**, including what a program has to change to use
it.

---

© 2026 Samuel Sáez López — UPCT — AGPL-3.0-or-later
