# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""Widgets the programs share: the status bar, the colour legend and the
number box."""
from .legend import ColourScaleLegend, StatusIndicators, ToggleLabel
from .number_box import NumberBox
from .status_bar import ElidingStatusBar, OgrStatusBar

__all__ = ["ColourScaleLegend", "StatusIndicators", "ToggleLabel",
           "ElidingStatusBar", "OgrStatusBar", "NumberBox"]
