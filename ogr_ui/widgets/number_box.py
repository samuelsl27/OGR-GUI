# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
The number box of the suite (OGR GUI 0.1.4, spec 005).

A ``QDoubleSpinBox`` follows the locale of the **machine**, not the
language of the program: on a machine configured for Spain it shows
``2,500`` and reads ``2.5`` as 25, a range or a tolerance ten times too
large with no warning (OGR FEM2D, T37 of its spec 006). And with the C or
an English locale it takes a comma as a thousands separator: ``1,000`` is
a thousand.

:class:`NumberBox` is a ``QDoubleSpinBox`` that does neither, on any
machine and in any language (the owner's decision of 2026-11-28):

* it shows the value with a decimal point and no thousands separator,
  written by :func:`ogr_ui.numbers.format_number`;
* it lets in a sign, figures, **one** point and an exponent. A comma, a
  second point or a letter does not go in, typed or pasted: the box keeps
  what it had, so what is written is always the number used;
* what is half written (``-``, ``1e``) or out of range goes back to the
  last value when the box is left, as a Qt box does.

Everything else is Qt's: the range, the decimals (to which Qt rounds the
value), the step, the prefix and the suffix, the special text of the
minimum. With ``scientific`` the value is shown as ``1.500e+03``, with
``decimals()`` places; the value is still rounded by Qt to ``decimals()``
places, so a box for small numbers needs enough of them.

The box sets a locale of its own (the C one, rejecting group separators)
and never the application's default one.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import re

from PySide6.QtGui import QValidator
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QDoubleSpinBox

from ogr_ui.numbers import format_number, read_number

#: What the box takes while it is being written: a sign, figures, one
#: point and an exponent, each perhaps not finished yet.
_WRITING = re.compile(r"[-+]?\d*(?:\.\d*)?(?:[eE][-+]?\d*)?")


def _c_locale() -> QLocale:
    loc = QLocale.c()
    loc.setNumberOptions(QLocale.NumberOption.OmitGroupSeparator
                         | QLocale.NumberOption.RejectGroupSeparator)
    return loc


class NumberBox(QDoubleSpinBox):
    """A ``QDoubleSpinBox`` that shows and takes a decimal point, and only
    a point, whatever the machine's locale and the program's language."""

    def __init__(self, parent=None, scientific: bool = False):
        super().__init__(parent)
        self._scientific = bool(scientific)
        self.setLocale(_c_locale())
        self.setGroupSeparatorShown(False)

    # ------------------------------------------------------------------
    def _body(self, text: str) -> str:
        t = text
        if self.prefix() and t.startswith(self.prefix()):
            t = t[len(self.prefix()):]
        if self.suffix() and t.endswith(self.suffix()):
            t = t[:-len(self.suffix())]
        return t.strip()

    def _is_special(self, text: str) -> bool:
        special = self.specialValueText()
        return bool(special) and text == special

    def textFromValue(self, value: float) -> str:  # noqa: N802 (Qt API)
        return format_number(value, self.decimals(),
                             scientific=self._scientific)

    def valueFromText(self, text: str) -> float:  # noqa: N802 (Qt API)
        if self._is_special(text):
            return self.minimum()
        try:
            return read_number(self._body(text))
        except ValueError:
            return self.value()

    def validate(self, text: str, pos: int):
        if self._is_special(text):
            return QValidator.State.Acceptable, text, pos
        body = self._body(text)
        if not _WRITING.fullmatch(body):
            return QValidator.State.Invalid, text, pos
        try:
            value = read_number(body)
        except ValueError:
            return QValidator.State.Intermediate, text, pos
        if self.minimum() <= value <= self.maximum():
            return QValidator.State.Acceptable, text, pos
        return QValidator.State.Intermediate, text, pos

    def fixup(self, text: str) -> str:
        # Qt's fixup takes group separators out; there are none to take
        return text
