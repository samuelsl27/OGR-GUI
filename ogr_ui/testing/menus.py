# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
Rule 3 of the suite, the same in every program: **every action can be
reached from a menu**, and every menu entry that is disabled says why.

From OGR Slip2D v0.1.486, where they were two test files of that program:

* ``tests/test_menu_reachability_v142.py`` (v0.1.42). A whole module was
  implemented, tested and published **invisible**: the groundwater
  interface, the probabilistic one and the support back analysis had their
  actions registered and never added to the menu bar (twelve actions).
  :func:`unreachable` walks the REAL menu bar of a window, submenus
  included, and names every registered action it does not find.
* ``tests/test_disabled_reasons_v1294.py`` (v0.1.294, D289b). With the
  Fusion and windows11 styles a disabled entry can say something only on
  the status bar (:mod:`ogr_ui.disabled_reasons`), and only if it has a
  status tip: seven entries of a new project were grey and silent.
  :func:`silent_disabled` names those.

The window is the program's; these functions only read its menu bar. A
program's test reads, for example::

    from ogr_ui.testing import menus
    assert not menus.unreachable(window, window.actions_by_key)

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

from typing import Iterable, Mapping


def menu_actions(window) -> list:
    """Every action that is an entry of a menu of ``window``'s menu bar,
    submenus walked, in menu order (the entries that open a submenu are not
    themselves listed)."""
    found = []

    def walk(menu):
        for act in menu.actions():
            sub = act.menu()
            if sub is not None:
                walk(sub)
            elif not act.isSeparator():
                found.append(act)

    for act in window.menuBar().actions():
        if act.menu() is not None:
            walk(act.menu())
    return found


def menu_texts(window) -> set:
    """The texts of :func:`menu_actions`."""
    return {a.text() for a in menu_actions(window) if a.text()}


def unreachable(window, actions: Mapping, allowed_absent: Iterable = ()) -> list:
    """The keys of ``actions`` (``{key: QAction}``, the program's registry)
    whose action is in no menu of the menu bar, less ``allowed_absent``
    (an action driven only from a tool bar or the canvas, each a decision).

    An action counts as reached when it IS an entry of a menu, and also when
    an entry has its text: Slip2D compared texts, and a menu entry built as a
    second ``QAction`` for the same command reaches the user all the same.
    """
    entries = menu_actions(window)
    ids = {id(a) for a in entries}
    texts = {a.text() for a in entries if a.text()}
    skip = set(allowed_absent)
    return sorted(key for key, act in actions.items()
                  if key not in skip and act.text()
                  and id(act) not in ids and act.text() not in texts)


def silent_disabled(window, actions: Mapping = None) -> list:
    """The menu entries that are disabled and say nothing (no status tip).

    With ``actions`` (``{key: QAction}``), their keys; without it, the texts
    of every disabled entry of the menu bar."""
    entries = menu_actions(window)
    if actions is None:
        return sorted(a.text() for a in entries
                      if not a.isEnabled() and not a.statusTip())
    ids = {id(a) for a in entries}
    return sorted(k for k, a in actions.items()
                  if id(a) in ids and not a.isEnabled() and not a.statusTip())
