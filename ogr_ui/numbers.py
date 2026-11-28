# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
How a number is written on screen and read back (OGR GUI 0.1.4, spec 005),
without Qt.

The decimal mark is **always the point**, in English and in Spanish and
whatever the machine's locale, with no thousands separator: the owner's
decision of 2026-11-28, when OGR FEM2D asked for one way of writing the
numbers of the suite. It is the notation of the CSV tables and of the
numerical reports, so what is on screen reads as what is in a file.

* :func:`format_number` writes ``value`` with ``decimals`` places, in
  scientific notation if asked, with a ``+`` if asked. Python's own
  format, which never looks at the locale: it is what the legend, the
  contour bands and the status bar wrote in 0.1.3, character for
  character.
* :func:`read_number` reads a sign, figures, **one** point and an
  exponent, with spaces only around them. A comma, a second point, a
  space or an underscore inside, ``nan`` and ``inf`` are refused with
  ``ValueError``: one point is always the decimal mark (``1.000`` is 1,
  never a thousand).

The number box of the dialogs (:class:`ogr_ui.widgets.NumberBox`) writes
and reads with these two.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import math
import re

#: A number as it can be written: a sign, figures with at most one point,
#: and an exponent. No comma, ever (spec 005, RF-6 and RF-7).
NUMBER = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?")


def format_number(value: float, decimals: int = 3, scientific: bool = False,
                  signed: bool = False) -> str:
    """``value`` with ``decimals`` places (none below zero), a decimal
    point and no thousands separator; in scientific notation
    (``1.25e+03``) if ``scientific``, with a ``+`` before a positive one
    if ``signed``."""
    d = max(0, int(decimals))
    kind = "e" if scientific else "f"
    sign = "+" if signed else ""
    return format(float(value), f"{sign}.{d}{kind}")


def read_number(text: str) -> float:
    """The number ``text`` writes, or ``ValueError``: a sign, figures,
    one decimal point and an exponent, with spaces only around it."""
    body = str(text).strip()
    if not NUMBER.fullmatch(body):
        raise ValueError(f"not a number written with a decimal point: {text!r}")
    value = float(body)
    if not math.isfinite(value):
        raise ValueError(f"not a finite number: {text!r}")
    return value
