# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
What a typed point means (OGR GUI 0.1.3, spec 004), without Qt.

:func:`read_point` reads the text of the X,Y entry of the status bar, or
of any other field that takes a point:

* **absolute**: two numbers separated by ``;`` (``1,5; 2,5``), by spaces
  with or without a comma just before them (``1,5 2,5``, ``1.5, 2.5``), or
  by one comma with no spaces, the decimal mark then being the point
  (``1.5,2.5``, ``3,4``);
* **relative** to a reference point: ``@dx, dy``, the two numbers by the
  same rules;
* **polar** from it: ``@distance<angle``, the angle in degrees from +x,
  anticlockwise. A cosine or a sine within 1e-15 of zero is zero, so
  ``@1<90`` is exactly one up.

Each number has a point or a comma as its decimal mark, a sign and an
exponent. What is ambiguous (``1,5,2,5``) or not a point is refused with
:class:`PointEntryError`, whose text says how to write it: nothing is
guessed (design reference D-7). The rules are OGR FEM2D's (its spec 006,
D10 and D12), which asked for this.

The reference point and the units are the program's: the reader adds and
returns numbers. The messages are English keys of ``tr()``; whoever shows
them translates them.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import math
import re
from typing import Optional

Point = tuple[float, float]

#: The reasons a typed point is refused (keys of ``tr()``).
WRITE_A_POINT = ("Write a point as x, y (or x; y with decimal commas), "
                 "@dx, dy or @distance<angle.")
WRITE_A_POLAR = ("Write a polar point as @distance<angle, with the angle "
                 "in degrees.")
NEEDS_A_FIRST = "A relative point needs a first point: give it as x, y."

_NUMBER = re.compile(r"[-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][-+]?\d+)?")

#: Below this, a cosine or a sine of the polar angle is zero.
_ZERO = 1e-15


class PointEntryError(ValueError):
    """A typed point that cannot be read; its text is the English key of
    the reason."""


def _number(text: str, reason: str) -> float:
    if not _NUMBER.fullmatch(text):
        raise PointEntryError(reason)
    value = float(text.replace(",", "."))
    if not math.isfinite(value):
        raise PointEntryError(reason)
    return value


def _pair(body: str) -> Point:
    body = body.strip()
    if ";" in body:
        parts = [p.strip() for p in body.split(";")]
    else:
        parts = body.split()
        if len(parts) == 2 and parts[0].endswith(","):
            parts[0] = parts[0][:-1]                  # "1.5, 2.5"
        elif len(parts) == 1 and body.count(",") == 1:
            parts = body.split(",")                   # "1.5,2.5", "3,4"
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
