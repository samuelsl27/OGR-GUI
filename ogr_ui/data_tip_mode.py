# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
How much a data tip says: nothing, the identity of the object, or all of it.

From OGR Slip2D's ``ogr_gui/data_tips.py`` (v0.1.486), which also builds
the tips themselves out of the limit-equilibrium labels and so stays in that
program. Only the setting is shared: the Snap dialog edits it.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

from enum import Enum


class DataTipMode(Enum):
    NONE = "none"
    MINIMUM = "min"
    MAXIMUM = "max"
