# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
OGR GUI — the interface pieces the programs of the OpenGeoRock Suite
share: the look (themes, icons), the language (``tr()``), the snap engine,
the status bar and the colour legend, the contour settings, background
tasks, saved preferences, and the guards that keep a Qt window usable
(dialog sizes, button floors, the mouse wheel, the garbage collector).

The distribution is ``ogr-gui`` (repository ``samuelsl27/OGR-GUI``); the
package is imported as ``ogr_ui``, because OGR Slip2D's own interface is
the package ``ogr_gui`` and the two must be able to live in one
environment.

It imports neither the core nor any program: no ``ogr_core``, no
``ogr_slip2d``, ``ogr_fem2d`` or ``ogr_data``, no ``mcp``. A test reads
the code and ``sys.modules`` for that (``tests/test_layering_v010.py``).

Developer: Samuel Sáez López — PhD Student, UPCT
"""
__version__ = "0.1.4.dev0"
