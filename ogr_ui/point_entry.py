# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
What a typed point means (OGR GUI 0.1.3, spec 004; 0.2.0, spec 006),
without Qt.

:func:`read_point` reads the text of the X,Y entry of the status bar, or
of any other field that takes a point:

* **absolute**: two numbers separated by **one comma**, with or without
  spaces around it (``1.5,2.5``, ``1.5, 2.5``);
* **relative** to a reference point: ``@dx,dy``, the two numbers by the
  same rule;
* **polar** from it: ``@distance<angle``, the angle in degrees from +x,
  anticlockwise. A cosine or a sine within 1e-15 of zero is zero, so
  ``@1<90`` is exactly one up.

Each number is read by :func:`ogr_ui.numbers.read_number`, as the number
boxes read theirs: a sign, figures, a decimal **point** and an exponent.
Since 0.2.0 (spec 006, the owner's criterion of 2026-11-28) the comma only
separates the coordinates: a decimal comma (``1,5; 2,5``), a lone space
(``1.5 2.5``) and a semicolon (``1.5;2.5``) are refused, as is anything
that is not one comma between two numbers. A refusal is a
:class:`PointEntryError` whose text says how to write a point: nothing is
guessed (design reference D-7). ``1,5`` is the point (1, 5).

The reference point and the units are the program's: the reader adds and
returns numbers. The messages are English keys of ``tr()``; whoever shows
them translates them.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import math
from typing import Optional

from ogr_ui.numbers import read_number

Point = tuple[float, float]

#: The reasons a typed point is refused (keys of ``tr()``).
WRITE_A_POINT = ("Write a point as x, y with a decimal point (1.5, 2.5), "
                 "@dx, dy or @distance<angle.")
WRITE_A_POLAR = ("Write a polar point as @distance<angle, with the angle "
                 "in degrees.")
NEEDS_A_FIRST = "A relative point needs a first point: give it as x, y."

#: Below this, a cosine or a sine of the polar angle is zero.
_ZERO = 1e-15


class PointEntryError(ValueError):
    """A typed point that cannot be read; its text is the English key of
    the reason."""


def _number(text: str, reason: str) -> float:
    try:
        return read_number(text)
    except ValueError:
        raise PointEntryError(reason) from None


def _pair(body: str) -> Point:
    # 0.2.0 (spec 006) -- exactly one comma between two numbers
    parts = body.split(",")
    if len(parts) != 2:
        raise PointEntryError(WRITE_A_POINT)
    return (_number(parts[0], WRITE_A_POINT),
            _number(parts[1], WRITE_A_POINT))


def as_reference(reference) -> Optional[Point]:
    if reference is None:
        return None
    ok = (isinstance(reference, (tuple, list)) and len(reference) == 2
          and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                  and math.isfinite(v) for v in reference))
    if not ok:
        raise ValueError(
            f"the reference point must be two finite numbers, not "
            f"{reference!r}")
    return float(reference[0]), float(reference[1])


def read_point(text: str, reference=None) -> Point:
    """The absolute point ``text`` means; ``@...`` is measured from
    ``reference`` (``None``: there is none, and a relative point is
    refused). Raises :class:`PointEntryError` with the reason, and
    ``ValueError`` for a reference that is not two finite numbers."""
    ref = as_reference(reference)
    t = (text or "").strip()
    if not t.startswith("@"):
        point = _pair(t)
    else:
        if ref is None:
            raise PointEntryError(NEEDS_A_FIRST)
        body = t[1:].strip()
        if "<" in body:
            d, a = body.split("<", 1)
            r = _number(d.strip(), WRITE_A_POLAR)
            angle = math.radians(_number(a.strip(), WRITE_A_POLAR))
            c, s = math.cos(angle), math.sin(angle)
            c = 0.0 if abs(c) < _ZERO else c
            s = 0.0 if abs(s) < _ZERO else s
            point = (ref[0] + r * c, ref[1] + r * s)
        else:
            dx, dy = _pair(body)
            point = (ref[0] + dx, ref[1] + dy)
    if not all(math.isfinite(v) for v in point):
        raise PointEntryError(WRITE_A_POINT)
    return point
