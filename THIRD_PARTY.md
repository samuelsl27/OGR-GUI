# Third-party notices

OGR GUI is released under the AGPL-3.0-or-later (see [`LICENSE`](LICENSE)). It depends on the
following works, which are distributed under their own licences and are not part of this
repository. All of them are compatible with the AGPL-3.0-or-later.

## Icons

The icons the interface shows (`ogr_ui/resources/icons.py`) are drawn from **Font Awesome 6 Free**
by Fonticons, Inc. (https://fontawesome.com), through **qtawesome**:

- Font Awesome Free icons: **CC BY 4.0** (https://creativecommons.org/licenses/by/4.0/). This
  notice is the attribution that licence asks for.
- Font Awesome Free fonts: **SIL OFL 1.1** (https://openfontlicense.org).
- qtawesome (https://github.com/spyder-ide/qtawesome): **MIT**.

The icons are used as published, recoloured at run time; none is modified in its drawing.

## Libraries

| Library | Licence | Used for |
|---|---|---|
| PySide6 (Qt for Python) | LGPL-3.0 | the whole interface |
| qtawesome | MIT | the icons (above) |
| Matplotlib | Matplotlib License (PSF-based) | the non-modal XY chart |

The tests also use **OGR Core** (`ogr-core`, AGPL-3.0-or-later, the same author) for the suite's
test runner. It is not a dependency of the package.
