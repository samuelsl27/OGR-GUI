# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
Rule 3 of the suite, as each program will check it: every action can be
reached from a menu, and a disabled menu entry says why on the status bar.

What this file protects, on a small window built here with a menu bar, a
submenu and a registry ``{key: QAction}`` that has one action in no menu,
one disabled entry with a status tip and one without:

* ``ogr_ui.testing.menus`` (OGR Slip2D v0.1.42; v0.1.294, D289b):
  ``menu_actions`` walks the real menu bar, submenus included, in menu
  order, without separators or the entries that open a submenu;
  ``menu_texts`` is their texts; ``unreachable`` names exactly the action in
  no menu (an entry with its text reaches the user all the same, and
  ``allowed_absent`` is a decision that takes it out); ``silent_disabled``
  names exactly the disabled entry with no status tip, by key or by text;
* ``ogr_ui.disabled_reasons`` (v0.1.288, D289; v0.1.328, D324):
  ``install`` puts one filter on every menu of the bar, submenus too; a
  pointer moving over a disabled entry puts its status tip on the window's
  status bar, and over an enabled entry or a silent one the filter does
  nothing; it never eats the event; it keeps no Python reference to its
  window; ``gate`` enables an action with no tip or disables it saying why
  (D289b: an enabled entry shows what it does, not what it needed).

From OGR Slip2D v0.1.486: ``tests/test_menu_reachability_v142.py``
(v0.1.42), ``tests/test_disabled_reasons_v1294.py`` (v0.1.294, D289b),
``tests/test_interpret_reasons_status_v1328.py`` (v0.1.328, D324: the
filter on another window, the pointer on a disabled entry, no reference to
the window) and ``tests/test_disabled_menus_v1288.py`` (v0.1.288, D289: the
hover). The menus of Slip2D's windows (Groundwater, Statistics, Support)
are Slip2D's; that a disabled entry is DRAWN paler is the themes' and is in
``test_themes_icons_v010``.

Every window and menu is closed and freed (rule 5); no menu is run with
``exec()``: a menu is opened with ``popup``, which does not block.
"""
from __future__ import annotations

import contextlib

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtWidgets import QApplication, QMenu

REASON = "Requires a finite-element groundwater method (Project Settings)."


def _app():
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _window():
    """``(window, registry, menus)``: File (Open, a disabled entry with its
    reason, a separator, Export ▸ (DXF, a silent disabled entry)) and View
    (Zoom All, and a second action for the Pan command); the registry also
    has an action in no menu, one with no text, and Pan."""
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QMainWindow
    from ogr_ui.disabled_reasons import gate
    app = _app()
    w = QMainWindow()
    bar = w.menuBar()
    m_file = bar.addMenu("File")
    acts = {}
    acts["open"] = QAction("Open...", w)
    acts["hydraulic"] = QAction("Define Hydraulic Properties...", w)
    gate(acts["hydraulic"], False, REASON)
    m_file.addAction(acts["open"])
    m_file.addAction(acts["hydraulic"])
    m_file.addSeparator()
    m_export = m_file.addMenu("Export")
    acts["export_dxf"] = QAction("Export DXF...", w)
    acts["silent"] = QAction("Export Mesh...", w)
    acts["silent"].setEnabled(False)
    m_export.addAction(acts["export_dxf"])
    m_export.addAction(acts["silent"])
    m_view = bar.addMenu("View")
    acts["zoom_all"] = QAction("Zoom All", w)
    m_view.addAction(acts["zoom_all"])
    # the same command built twice: the menu's entry is another QAction
    acts["pan"] = QAction("Pan", w)
    m_view.addAction(QAction("Pan", w))
    # registered and in no menu: the defect of v0.1.42
    acts["missing"] = QAction("Back Analysis...", w)
    # no text, nothing to reach (a tool bar's spacer, say)
    acts["blank"] = QAction(w)
    menus = {"file": m_file, "export": m_export, "view": m_view}
    try:
        yield w, acts, menus
    finally:
        for m in menus.values():
            m.hide()
        w.hide()
        w.deleteLater()
        app.processEvents()


def _move_over(menu, act, send=True, flt=None):
    """A pointer move over ``act`` on ``menu``, opened as the user has it
    (a menu never shown finds no action under a point). Through the event
    system when ``send``, else straight into ``flt``'s ``eventFilter``;
    returns what the filter answered, when called directly."""
    from PySide6.QtGui import QMouseEvent
    app = _app()
    menu.popup(menu.parentWidget().mapToGlobal(
        menu.parentWidget().rect().center()))
    app.processEvents()
    centre = QPointF(menu.actionGeometry(act).center())
    ev = QMouseEvent(QEvent.Type.MouseMove, centre,
                     QPointF(menu.mapToGlobal(centre.toPoint())),
                     Qt.NoButton, Qt.NoButton, Qt.NoModifier)
    if send:
        QApplication.sendEvent(menu, ev)
        app.processEvents()
        return None
    return flt.eventFilter(menu, ev)


# ======================================================================
class TestTheWalk:
    def test_menu_actions_in_menu_order(self):
        from ogr_ui.testing.menus import menu_actions
        with _window() as (w, acts, menus):
            found = menu_actions(w)
            assert [a.text() for a in found] == [
                "Open...", "Define Hydraulic Properties...",
                "Export DXF...", "Export Mesh...", "Zoom All", "Pan"]
            assert found[:2] == [acts["open"], acts["hydraulic"]]
            # neither separators nor the entry that opens Export
            assert not any(a.isSeparator() for a in found)
            assert not any(a.menu() is not None for a in found)

    def test_menu_texts(self):
        from ogr_ui.testing.menus import menu_texts
        with _window() as (w, acts, menus):
            assert menu_texts(w) == {
                "Open...", "Define Hydraulic Properties...",
                "Export DXF...", "Export Mesh...", "Zoom All", "Pan"}


class TestReachability:
    def test_exactly_the_action_in_no_menu(self):
        from ogr_ui.testing.menus import unreachable
        with _window() as (w, acts, menus):
            # Pan is reached by its text; the blank one has none
            assert unreachable(w, acts) == ["missing"]

    def test_an_allowed_absence_is_a_decision(self):
        from ogr_ui.testing.menus import unreachable
        with _window() as (w, acts, menus):
            assert unreachable(w, acts, allowed_absent={"missing"}) == []

    def test_adding_it_to_a_menu_reaches_it(self):
        from ogr_ui.testing.menus import unreachable
        with _window() as (w, acts, menus):
            menus["export"].addAction(acts["missing"])
            assert unreachable(w, acts) == []


class TestEveryDisabledEntrySaysWhy:
    def test_by_key_exactly_the_silent_one(self):
        from ogr_ui.testing.menus import silent_disabled
        with _window() as (w, acts, menus):
            assert silent_disabled(w, acts) == ["silent"]

    def test_by_text_without_a_registry(self):
        from ogr_ui.testing.menus import silent_disabled
        with _window() as (w, acts, menus):
            assert silent_disabled(w) == ["Export Mesh..."]

    def test_a_disabled_action_in_no_menu_is_not_counted(self):
        """It is ``unreachable``'s: nobody can see it grey."""
        from ogr_ui.testing.menus import silent_disabled
        with _window() as (w, acts, menus):
            acts["missing"].setEnabled(False)
            assert silent_disabled(w, acts) == ["silent"]

    def test_gated_with_a_reason_it_is_silent_no_more(self):
        from ogr_ui.disabled_reasons import gate
        from ogr_ui.testing.menus import silent_disabled
        with _window() as (w, acts, menus):
            gate(acts["silent"], False, "Requires a mesh.")
            assert silent_disabled(w, acts) == []


class TestGate:
    def test_enabled_without_a_reason_disabled_with_it(self):
        from PySide6.QtGui import QAction
        from ogr_ui.disabled_reasons import gate
        _app()
        act = QAction("Compute Groundwater")
        try:
            gate(act, False, REASON)
            assert not act.isEnabled() and act.statusTip() == REASON
            gate(act, True, REASON)
            assert act.isEnabled() and act.statusTip() == ""
            # anything with a truth value
            gate(act, [], REASON)
            assert not act.isEnabled() and act.statusTip() == REASON
            gate(act, 1, REASON)
            assert act.isEnabled() and act.statusTip() == ""
        finally:
            act.deleteLater()


class TestTheFilter:
    def test_it_is_on_every_menu_submenus_too(self):
        from ogr_ui import disabled_reasons
        with _window() as (w, acts, menus):
            flt = disabled_reasons.install(w)
            assert flt.parent() is w
            assert w.findChildren(disabled_reasons.DisabledReasonFilter) \
                == [flt]
            # installed on each: a move over the submenu's entry is seen
            gate_reason = "Requires a mesh."
            disabled_reasons.gate(acts["silent"], False, gate_reason)
            _move_over(menus["export"], acts["silent"])
            assert w.statusBar().currentMessage() == gate_reason

    def test_the_pointer_on_a_disabled_entry_puts_its_reason_on_the_bar(self):
        from ogr_ui import disabled_reasons
        with _window() as (w, acts, menus):
            disabled_reasons.install(w)
            assert w.statusBar().currentMessage() == ""
            _move_over(menus["file"], acts["hydraulic"])
            assert w.statusBar().currentMessage() == REASON

    def test_control_without_the_filter_the_bar_stays_empty(self):
        """Qt does not make a disabled entry the menu's current one with
        this style, so its status tip alone never shows."""
        with _window() as (w, acts, menus):
            _move_over(menus["file"], acts["hydraulic"])
            assert w.statusBar().currentMessage() == ""

    def test_nothing_for_an_enabled_entry_or_a_silent_one(self):
        from ogr_ui.disabled_reasons import DisabledReasonFilter
        with _window() as (w, acts, menus):
            flt = DisabledReasonFilter(w)
            acts["open"].setStatusTip("Open a project.")
            # straight into the filter: Qt itself may show an enabled
            # entry's tip, and that is not the filter's doing
            assert _move_over(menus["file"], acts["open"], send=False,
                              flt=flt) is False
            assert w.statusBar().currentMessage() == ""
            assert _move_over(menus["export"], acts["silent"], send=False,
                              flt=flt) is False
            assert w.statusBar().currentMessage() == ""
            # and for the disabled one with its reason, the same call does
            assert _move_over(menus["file"], acts["hydraulic"], send=False,
                              flt=flt) is False
            assert w.statusBar().currentMessage() == REASON

    def test_it_looks_at_menus_and_mouse_moves_only(self):
        from PySide6.QtCore import QEvent as E
        from ogr_ui.disabled_reasons import DisabledReasonFilter
        with _window() as (w, acts, menus):
            flt = DisabledReasonFilter(w)
            assert flt.eventFilter(w, E(E.Type.MouseMove)) is False
            assert flt.eventFilter(menus["file"], E(E.Type.Show)) is False
            assert w.statusBar().currentMessage() == ""

    def test_it_keeps_no_python_reference_to_its_window(self):
        from ogr_ui import disabled_reasons
        with _window() as (w, acts, menus):
            flt = disabled_reasons.install(w)
            assert not any(v is w for v in vars(flt).values())
            assert not any(v is flt for v in vars(w).values())
