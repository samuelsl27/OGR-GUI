# OGR GUI

**The interface pieces the programs of the [OpenGeoRock](https://opengeorock.org) suite share** —
the light and dark themes, the icons, `tr()` and its dictionary, the snap engine, the status bar,
the colour legend, the contour settings, background tasks, saved preferences, and the guards that
keep a Qt window usable.

[Versión en español](README.es.md)

> **Latest release: 0.1.0.** The pieces are those of
> [OGR Slip2D](https://github.com/samuelsl27/OGR-Slip2D)'s interface at its v0.1.486 (commit
> `03b6c2d`), copied without changing that program. The distribution is `ogr-gui`; the package is
> imported as **`ogr_ui`**, because `ogr_gui` is OGR Slip2D's own interface and the two must be able
> to share an environment.

## What it is, and what it is not

It is what two programs need to look and behave the same: the style sheets and the colour of each
role (`ogr_ui.themes`), ~90 semantic icon keys (`ogr_ui.resources.icons`), one `tr()` with the
Spanish of these pieces (`ogr_ui.i18n`; each program adds its own dictionary), SNAP / ORTHO / OSNAP
with tolerances in pixels (`ogr_ui.canvas.snap_engine`), and the checks of two rules of the suite
for each program's tests: every visible text goes through `tr()`, every action is in a menu
(`ogr_ui.testing`).

It is not a program's window, canvas or results viewer: those mix what is shared with what each
program computes, and each program writes its own on these pieces.

It does **not** depend on OGR Core. Each program pins its own tag of the core, and pip refuses two
different git references to the same distribution; the two pieces that read the core in OGR Slip2D
take what they need through a small interface instead (`SnapShape`, `install_progress`).

## Using it from a program

```toml
# pyproject.toml of the program
dependencies = ["ogr-gui @ git+https://github.com/samuelsl27/OGR-GUI@v0.1.0"]
```

```python
from ogr_ui.i18n import add_translations, tr
from ogr_ui.themes import apply_theme
from ogr_ui.user_prefs import Preferences

add_translations("es", MY_SPANISH)            # the program's own texts
prefs = Preferences("OGR FEM2D", "ogr-fem2d")  # its name in QSettings
apply_theme(app, prefs.saved_theme() or "light")
```

Which program pins which version: [`docs/consumidores.md`](docs/consumidores.md) (in Spanish).

## Development

You need Python 3.11 or newer (CI runs 3.11, 3.12 and 3.13 on Linux, Windows and macOS) and git.

```bash
git clone https://github.com/samuelsl27/OGR-GUI.git
cd OGR-GUI
python -m venv .venv && source .venv/bin/activate
pip install -e ".[test]"
QT_QPA_PLATFORM=offscreen python tests/_runner.py
```

The `[test]` extra installs OGR Core from the tag it pins, for the suite's test runner and its leak
check only. The suite is green when its totals say `Failed: 0` with no `[LEAK]`. The working rules
are in [`AGENTS.md`](AGENTS.md) (in Spanish), the same as in the rest of the suite.

## Licence

**GNU Affero General Public License v3.0 or later** (AGPL-3.0-or-later). The
full text is in [`LICENSE`](LICENSE). The icons are Font Awesome Free (CC BY 4.0):
see [`THIRD_PARTY.md`](THIRD_PARTY.md).

In practice:

- You may use OGR Suite freely, **including for professional engineering
  work**, and bill that work without paying or publishing anything. Running a
  program is not a restricted activity.
- If you **modify** it and let others use your version **remotely over a
  network** (a web service or SaaS), you must offer them the source of your
  version. Charging for that service is allowed; keeping it closed is not.
- **There is no warranty of any kind.** Results must be checked against
  independent calculations before anything is based on them. A project is
  signed by a person, not by a program.

Every file carries its SPDX identifier, and a test fails if any is missing.
Contributions are accepted under the terms of [`CLA.md`](CLA.md); see
[`CONTRIBUTING.md`](CONTRIBUTING.md).

© 2026 Samuel Sáez López — Universidad Politécnica de Cartagena.
