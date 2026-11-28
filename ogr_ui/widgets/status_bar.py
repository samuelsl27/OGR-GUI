# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
Custom status bar with SNAP / GRID / ORTHO / OSNAP toggles, live
coordinate readout, and a manual X,Y entry field for typing an exact
point (Slip2D v0.1.3). Since OGR GUI 0.1.3 (spec 004, asked by OGR FEM2D)
the entry reads relative and polar points and the decimal comma with
:mod:`ogr_ui.point_entry`, from the reference point the program gives
(:meth:`OgrStatusBar.set_point_reference`), and says in the bar why it
refuses what it cannot read.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import time
from typing import Optional

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QDoubleValidator, QMouseEvent
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QStatusBar,
    QStyle,
    QStyleOptionFrame,
    QWidget,
)

from ogr_ui.i18n import tr
from ogr_ui.numbers import format_number


# ----------------------------------------------------------------------
class _ToggleLabel(QLabel):
    """A QLabel that acts like a toggle button."""
    toggled = Signal(bool)

    def __init__(self, text: str, active: bool = False, parent=None) -> None:
        super().__init__(text, parent)
        self._active = active
        self.setCursor(Qt.PointingHandCursor)
        self._refresh()

    def isChecked(self) -> bool:  # noqa: N802
        return self._active

    def setChecked(self, v: bool) -> None:  # noqa: N802
        if v != self._active:
            self._active = v
            self._refresh()
            self.toggled.emit(self._active)

    def mousePressEvent(self, ev: QMouseEvent) -> None:  # noqa: N802
        self.setChecked(not self._active)

    def _refresh(self) -> None:
        # v0.1.316 (D301) — "on" paints its own background, so it reads on
        # either theme; "off" is text on the bar's, and asks the theme
        from ogr_ui.themes import theme_color
        self.setStyleSheet(
            "padding: 2px 8px; border-radius: 3px; "
            + ("background: #b9d7f7; color: #10305a; font-weight: 500;"
               if self._active else "background: transparent; color: %s;"
               % theme_color("toggle_off"))
        )


# ----------------------------------------------------------------------
class _CoordInput(QLineEdit):
    """Compact X,Y entry field (OGR GUI 0.1.3, spec 004).

    On Enter it reads its text with :func:`ogr_ui.point_entry.read_point`:
    an absolute point (``1,5; 2,5``, ``12.5, 3.2``, ``1.5,2.5``), one
    relative to the reference point the program gives (``@dx, dy``), or a
    polar one from it (``@distance<angle``, degrees). A point read is
    emitted by :attr:`coords_submitted` (x, y), always absolute, and the
    field is emptied. A text that cannot be read stays where it is, for
    correcting, and :attr:`point_refused` says why, translated. Any
    character can be typed: nothing is read until Enter.
    """
    coords_submitted = Signal(float, float)
    point_refused = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._reference = None
        # what can be typed: notation, the same in every language
        self.setPlaceholderText("x, y · @dx, dy · @d<a")
        # as wide as the whole placeholder in its own font (sizeHint), and
        # no wider: the messages of the bar keep their room
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setToolTip(tr(
            "Type a point and press Enter: x, y (or x; y with decimal "
            "commas), @dx, dy from the last point, or @distance<angle in "
            "degrees."))
        self.returnPressed.connect(self._submit)

    def sizeHint(self) -> QSize:  # noqa: N802
        """Room for the whole placeholder, measured with the font and the
        style the field has now (they change with the theme)."""
        opt = QStyleOptionFrame()
        self.initStyleOption(opt)
        m = self.textMargins()
        fm = self.fontMetrics()
        # 2 px each side: QLineEdit's own horizontal margin
        inner = QSize(fm.horizontalAdvance(self.placeholderText()) + 4
                      + m.left() + m.right(), fm.height())
        return self.style().sizeFromContents(
            QStyle.CT_LineEdit, opt, inner, self)

    def minimumSizeHint(self) -> QSize:  # noqa: N802
        return self.sizeHint()

    def set_reference(self, point) -> None:
        """The point ``@...`` is measured from, in the program's units, or
        ``None`` for none. One that is not two finite numbers raises
        ``ValueError`` here, where it is given."""
        from ogr_ui.point_entry import as_reference
        self._reference = as_reference(point)

    def reference(self):
        return self._reference

    def _submit(self) -> None:
        from ogr_ui.point_entry import PointEntryError, read_point
        txt = self.text()
        if not txt.strip():
            return
        try:
            x, y = read_point(txt, self._reference)
        except PointEntryError as exc:
            self.point_refused.emit(tr(str(exc)))
            return
        self.coords_submitted.emit(x, y)
        self.clear()


# ======================================================================
class ElidingStatusBar(QStatusBar):
    """A status bar whose message ends in «…» where its indicators begin,
    with the whole text as the bar's tooltip while it lasts (v0.1.328, D325).

    QStatusBar draws its message under whatever is permanent on the right,
    so the end of a long one was hidden behind SNAP / GRID / ORTHO / OSNAP:
    «… un método de agua por rejilla (…), que ader…». The text is cut to the
    room the indicators leave and cut again when the bar changes size,
    without restarting the message's time.

    ``currentMessage()`` answers the WHOLE message: what the window said,
    not what fitted. A message Qt shows by itself (an action's status tip,
    sent from C++) is cut the same way since v0.1.418 (D355): it never goes
    through ``showMessage`` here, and it was hidden behind the indicators
    with no «…» -- which is how the reason of a disabled action reached the
    reader, half of it.
    """

    #: Room kept between the message and the first indicator, in pixels.
    GAP_PX = 8

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._full = ""
        self._shown = ""
        self._until: Optional[float] = None
        self.messageChanged.connect(self._on_message_changed)

    def showMessage(self, text: str, timeout: int = 0) -> None:  # noqa: N802
        self._full = text or ""
        self._until = (time.monotonic() + timeout / 1000.0
                       if timeout and timeout > 0 else None)
        self._show(timeout)

    def currentMessage(self) -> str:  # noqa: N802
        shown = super().currentMessage()
        if shown and shown == self._shown:
            return self._full
        return shown

    def clearMessage(self) -> None:  # noqa: N802
        self._full = self._shown = ""
        self._until = None
        self.setToolTip("")
        super().clearMessage()

    def message_room(self) -> int:
        """The width, in pixels, the message has left of the indicators."""
        right = self.width()
        for child in self.findChildren(QWidget, "", Qt.FindDirectChildrenOnly):
            if child.isVisible() and child.x() > 0:
                right = min(right, child.x())
        return right - self.GAP_PX

    def _show(self, timeout: int) -> None:
        text = self._full
        room = self.message_room()
        if self.isVisible() and room > 0:
            text = self.fontMetrics().elidedText(self._full, Qt.ElideRight,
                                                 room)
        self._shown = text
        self.setToolTip(self._full if text != self._full else "")
        super().showMessage(text, timeout)

    def _on_message_changed(self, text: str) -> None:
        if not text:
            # the message's time ran out, or another took its place
            self._full = self._shown = ""
            self._until = None
            self.setToolTip("")
            return
        if text != self._shown:
            # A message Qt put here from C++ (the status tip of the action
            # under the pointer): shown again through ``_show``, whose own
            # message comes back here equal to ``_shown`` and stops
            self._full = text
            self._until = None
            self._show(0)

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        if not self._full or super().currentMessage() != self._shown:
            return
        if self._until is None:
            self._show(0)
            return
        left = int((self._until - time.monotonic()) * 1000)
        if left > 0:
            self._show(left)


# ======================================================================
class OgrStatusBar(ElidingStatusBar):
    """Status bar: hint message + snap toggles + X/Y readout + manual input."""

    snap_toggled = Signal(bool)
    grid_toggled = Signal(bool)
    ortho_toggled = Signal(bool)
    osnap_toggled = Signal(bool)
    manual_coords_submitted = Signal(float, float)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Coord readout
        self.coord_label = QLabel(tr("X: 0.000   Y: 0.000"))
        self.coord_label.setMinimumWidth(170)

        # Manual coord input
        self.coord_input = _CoordInput(self)
        self.coord_input.coords_submitted.connect(self.manual_coords_submitted.emit)
        self.coord_input.point_refused.connect(self.showMessage)

        # Toggle indicators
        self.snap = _ToggleLabel(tr("SNAP"), True)
        self.grid = _ToggleLabel(tr("GRID"), True)
        self.ortho = _ToggleLabel(tr("ORTHO"), False)
        self.osnap = _ToggleLabel(tr("OSNAP"), False)

        self.snap.toggled.connect(self.snap_toggled.emit)
        self.grid.toggled.connect(self.grid_toggled.emit)
        self.ortho.toggled.connect(self.ortho_toggled.emit)
        self.osnap.toggled.connect(self.osnap_toggled.emit)

        # Assemble — right side
        for w in (self.snap, self.grid, self.ortho, self.osnap):
            self.addPermanentWidget(w)
        self._extra_toggles: dict = {}
        self._sep = QLabel(" │ ")
        self.addPermanentWidget(self._sep)
        self.addPermanentWidget(self.coord_label)
        self.addPermanentWidget(QLabel("  "))  # spacer
        self.addPermanentWidget(QLabel(tr("Enter X,Y:")))
        self.addPermanentWidget(self.coord_input)
        self.retheme()

    # ------------------------------------------------------------------
    def set_point_reference(self, point) -> None:
        """The point a typed ``@dx, dy`` or ``@distance<angle`` is measured
        from (the last vertex, say), in the units the program shows; ``None``
        when there is none, and then a relative point is refused with its
        reason (spec 004)."""
        self.coord_input.set_reference(point)

    def retheme(self) -> None:
        """Colour the readout and the separator for the active theme, and
        the toggles that are off (v0.1.316, D301: #4a4a4a on the dark bar
        could hardly be read)."""
        from ogr_ui.themes import theme_color
        self.coord_label.setStyleSheet(
            "color: %s; font-family: monospace;" % theme_color("status_text"))
        self._sep.setStyleSheet("color: %s;" % theme_color("separator"))
        for t in (self.snap, self.grid, self.ortho, self.osnap,
                  *getattr(self, "_extra_toggles", {}).values()):
            t._refresh()

    def update_coords(self, x: float, y: float) -> None:
        # 0.1.4 (spec 005) -- always a decimal point, in every language
        self.coord_label.setText(
            f"X: {format_number(x, 3, signed=True)}   "
            f"Y: {format_number(y, 3, signed=True)}")

    # ------------------------------------------------------------------
    def add_toggle(self, text: str, active: bool = False):
        """Add another clickable indicator to the status bar.

        v0.1.51 — the bar shipped with SNAP / GRID / ORTHO / OSNAP hard
        wired. DATA TIPS needed one too, and a later phase will want
        others, so the bar grows through this instead of by editing its
        constructor each time.
        """
        if not hasattr(self, "_extra_toggles"):
            self._extra_toggles = {}
        existing = self._extra_toggles.get(text)
        if existing is not None:
            return existing
        label = _ToggleLabel(text, active)
        self.addPermanentWidget(label)
        self._extra_toggles[text] = label
        return label

    def toggle(self, text: str):
        """An indicator added with :meth:`add_toggle`, or None."""
        return getattr(self, "_extra_toggles", {}).get(text)
