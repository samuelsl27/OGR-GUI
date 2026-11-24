# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""What a program's canvas shares: the snap engine. The canvas itself is
each program's."""
from .snap_engine import SnapEngine, SnapKind, SnapPoint, SnapResult, SnapSettings, SnapShape

__all__ = ["SnapEngine", "SnapKind", "SnapPoint", "SnapResult", "SnapSettings", "SnapShape"]
