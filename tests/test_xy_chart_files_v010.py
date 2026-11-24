# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
A chart opens next to the model, never in front of it; a file dialog starts
where the user was working.

What this file protects:

* ``ogr_ui.xy_chart`` (OGR Slip2D v0.1.308, D311; v0.1.435, D413): a chart
  opens NON-modal (``exec()`` is replaced here by one that fails), visible,
  owned by its window and kept on ``window._chart_windows`` so Qt does not
  collect it; it plots exactly the series it is given, with their labels in
  a legend only when there is something to tell apart, the axes named and
  the scale asked (v0.1.269: logarithmic); two charts can be open at once,
  and a chart the user closed is let go (``setParent(None)``) when another
  opens;
* ``ogr_ui.file_folders`` (v0.1.418, D355): a file dialog of a window starts
  in the folder last used in that window, before any in the folder of the
  saved project, and otherwise in the user's Documents (never the working
  folder); a folder that no longer exists is passed over; the folder picked
  is remembered and a cancelled dialog changes nothing; a proposed file name
  goes inside the folder.

From OGR Slip2D v0.1.486: ``tests/test_fos_chart_v1308.py`` (v0.1.308,
D311: non-modal and kept), ``tests/test_interpret_charts_v1435.py``
(v0.1.435, D413: ``keep_chart``, a closed chart let go),
``tests/test_texts_details_v1418.py`` (v0.1.418, D355: where the dialogs
start) and ``tests/test_report_figures_v1339.py`` (the file dialog swapped
where ``file_folders`` looks it up). What those files check of Interpret,
the groundwater window and the report (their series, their identities, the
status bar) stays in Slip2D.

No real file dialog is opened: ``QFileDialog.getOpenFileName`` and
``getSaveFileName`` are swapped and put back; every chart is closed and let
go; ``exec()`` is put back (rule 5).
"""
from __future__ import annotations

import contextlib
import os
import tempfile
import types

from PySide6.QtWidgets import QApplication

_MISSING = object()


def _app():
    return QApplication.instance() or QApplication([])


@contextlib.contextmanager
def _swap(owner, name, value):
    raw = (owner.__dict__.get(name, _MISSING) if isinstance(owner, type)
           else getattr(owner, name))
    setattr(owner, name, value)
    try:
        yield
    finally:
        if raw is _MISSING:
            delattr(owner, name)
        else:
            setattr(owner, name, raw)


@contextlib.contextmanager
def _no_modals():
    """A modal dialog or message box fails the test instead of waiting for
    ever without a screen."""
    from PySide6.QtWidgets import QDialog, QMessageBox

    def modal(*a, **k):
        raise AssertionError("a modal window")

    with contextlib.ExitStack() as stack:
        stack.enter_context(_swap(QDialog, "exec", modal))
        for name in ("information", "warning", "critical", "question"):
            stack.enter_context(_swap(QMessageBox, name,
                                      staticmethod(modal)))
        yield


@contextlib.contextmanager
def _owner():
    """A main window to own the charts; every chart closed and freed."""
    from PySide6.QtWidgets import QMainWindow
    app = _app()
    w = QMainWindow()
    try:
        yield w
    finally:
        for dlg in list(getattr(w, "_chart_windows", [])):
            dlg.close()
            dlg.setParent(None)
            dlg.deleteLater()
        w.deleteLater()
        app.processEvents()


def _axes(dlg):
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
    canvases = dlg.findChildren(FigureCanvasQTAgg)
    assert len(canvases) == 1, canvases
    return canvases[0].figure.axes[0]


SERIES = [("Bishop", [0.0, 1e4, 1e6], [1.52, 1.31, 1.18]),
          ("Spencer", [0.0, 1e4, 1e6], [1.55, 1.34, 1.20])]


# ======================================================================
class TestTheChart:
    def test_it_is_not_modal_and_its_window_keeps_it(self):
        from ogr_ui.xy_chart import show_xy_chart
        with _owner() as w, _no_modals():
            dlg = show_xy_chart(w, "FS frente al tiempo", SERIES,
                                "Tiempo (s)", "FS")
            assert dlg is not None
            assert dlg.isVisible() and not dlg.isModal()
            assert dlg.parent() is w
            assert dlg in w._chart_windows
            assert dlg.windowTitle() == "FS frente al tiempo"

    def test_it_plots_the_series_it_is_given(self):
        from ogr_ui.xy_chart import show_xy_chart
        with _owner() as w, _no_modals():
            dlg = show_xy_chart(w, "t", SERIES, "Tiempo (s)", "FS",
                                marker="s")
            ax = _axes(dlg)
            lines = [(ln.get_label(), list(ln.get_xdata()),
                      list(ln.get_ydata())) for ln in ax.get_lines()]
            assert lines == [(lab, list(xs), list(ys))
                             for lab, xs, ys in SERIES]
            assert all(ln.get_marker() == "s" for ln in ax.get_lines())
            assert ax.get_xlabel() == "Tiempo (s)"
            assert ax.get_ylabel() == "FS"
            assert ax.get_yscale() == "linear"
            legend = ax.get_legend()
            assert legend is not None
            assert [t.get_text() for t in legend.get_texts()] == \
                ["Bishop", "Spencer"]

    def test_a_legend_only_with_something_to_tell_apart(self):
        from ogr_ui.xy_chart import show_xy_chart
        with _owner() as w, _no_modals():
            bare = show_xy_chart(w, "t", [("", [1, 2], [3, 4])], "x", "y")
            assert _axes(bare).get_legend() is None
            named = show_xy_chart(w, "t", [("Spencer", [1, 2], [3, 4])],
                                  "x", "y")
            assert _axes(named).get_legend() is not None

    def test_the_scale_it_is_asked(self):
        """v0.1.269: a convergence spans ten decades; log10 of the values
        would turn a zero change into -inf."""
        from ogr_ui.xy_chart import show_xy_chart
        with _owner() as w, _no_modals():
            dlg = show_xy_chart(w, "t", [("", [1, 2, 3], [1.0, 1e-5, 1e-10])],
                                "Iteración", "Residuo", yscale="log")
            ax = _axes(dlg)
            assert ax.get_yscale() == "log"
            assert list(ax.get_lines()[0].get_ydata()) == [1.0, 1e-5, 1e-10]

    def test_two_can_be_open_at_once(self):
        from ogr_ui.xy_chart import show_xy_chart
        with _owner() as w, _no_modals():
            first = show_xy_chart(w, "a", SERIES, "x", "y")
            second = show_xy_chart(w, "b", SERIES, "x", "y")
            assert first.isVisible() and second.isVisible()
            assert w._chart_windows == [first, second]


class TestKeepChart:
    def test_a_closed_chart_is_let_go_when_another_opens(self):
        from PySide6.QtWidgets import QDialog
        from ogr_ui.xy_chart import keep_chart
        with _owner() as w, _no_modals():
            first = keep_chart(w, QDialog(w))
            assert first.isVisible() and not first.isModal()
            first.close()
            second = keep_chart(w, QDialog(w))
            try:
                assert second in w._chart_windows
                assert first not in w._chart_windows
                # let go: no longer the window's child
                assert first.parent() is None
                assert second.parent() is w
            finally:
                first.deleteLater()

    def test_an_open_chart_is_kept(self):
        from PySide6.QtWidgets import QDialog
        from ogr_ui.xy_chart import keep_chart
        with _owner() as w, _no_modals():
            first = keep_chart(w, QDialog(w))
            second = keep_chart(w, QDialog(w))
            assert w._chart_windows == [first, second]
            assert first.parent() is w

    def test_an_owner_without_a_list_gets_one(self):
        from PySide6.QtWidgets import QDialog
        from ogr_ui.xy_chart import keep_chart
        with _owner() as w, _no_modals():
            assert not hasattr(w, "_chart_windows")
            dlg = keep_chart(w, QDialog(w))
            assert w._chart_windows == [dlg]


# ======================================================================
def _recording(answer=""):
    """A stand-in for a ``QFileDialog`` static: records the folder it was
    given and answers ``answer``."""
    calls = []

    def ask(parent, title, folder, filters, *a, **k):
        calls.append((parent, title, folder, filters))
        return answer, ("Todos (*)" if answer else "")
    return calls, staticmethod(ask)


def _documents():
    from PySide6.QtCore import QStandardPaths
    return (QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
            or os.path.expanduser("~"))


def _norm(path):
    return os.path.normcase(os.path.abspath(path))


class TestWhereAFileDialogStarts:
    def test_documents_first_never_the_working_folder(self):
        from ogr_ui.file_folders import start_folder
        _app()
        w = types.SimpleNamespace()
        assert start_folder(w) == _documents()
        w = types.SimpleNamespace(project=types.SimpleNamespace(
            file_path=None))
        assert start_folder(w) == _documents()
        assert _norm(start_folder(w)) != _norm(os.getcwd())

    def test_then_the_folder_of_the_saved_project(self):
        from pathlib import Path
        from ogr_ui.file_folders import start_folder
        _app()
        with tempfile.TemporaryDirectory() as tmp:
            for path in (Path(tmp) / "talud.ogr",
                         os.path.join(tmp, "talud.ogr")):
                w = types.SimpleNamespace(
                    project=types.SimpleNamespace(file_path=path))
                assert _norm(start_folder(w)) == _norm(tmp)

    def test_the_last_folder_of_the_window_wins(self):
        from ogr_ui.file_folders import start_folder
        _app()
        with tempfile.TemporaryDirectory() as saved, \
                tempfile.TemporaryDirectory() as last:
            w = types.SimpleNamespace(
                _last_folder=last,
                project=types.SimpleNamespace(
                    file_path=os.path.join(saved, "talud.ogr")))
            assert _norm(start_folder(w)) == _norm(last)

    def test_a_folder_that_is_gone_is_passed_over(self):
        from ogr_ui.file_folders import start_folder
        _app()
        with tempfile.TemporaryDirectory() as saved:
            gone = os.path.join(saved, "borrada")
            w = types.SimpleNamespace(
                _last_folder=gone,
                project=types.SimpleNamespace(
                    file_path=os.path.join(saved, "talud.ogr")))
            assert _norm(start_folder(w)) == _norm(saved)
            w.project.file_path = os.path.join(gone, "talud.ogr")
            assert start_folder(w) == _documents()


class TestTheDialogs:
    def test_open_starts_there_and_remembers_the_pick(self):
        from PySide6.QtWidgets import QFileDialog
        from ogr_ui.file_folders import get_open_file_name
        _app()
        w = types.SimpleNamespace()
        with tempfile.TemporaryDirectory() as tmp:
            picked = os.path.join(tmp, "plano.dxf")
            calls, ask = _recording(picked)
            with _swap(QFileDialog, "getOpenFileName", ask):
                got = get_open_file_name(w, "Importar DXF", "DXF (*.dxf)")
            assert got == (picked, "Todos (*)")
            assert calls == [(w, "Importar DXF", _documents(),
                              "DXF (*.dxf)")], calls
            assert _norm(w._last_folder) == _norm(tmp)
            # the next one starts in the folder of the pick
            calls, ask = _recording()
            with _swap(QFileDialog, "getOpenFileName", ask):
                get_open_file_name(w, "t", "*")
            assert _norm(calls[0][2]) == _norm(tmp)

    def test_a_cancelled_dialog_changes_nothing(self):
        from PySide6.QtWidgets import QFileDialog
        from ogr_ui.file_folders import get_open_file_name, get_save_file_name
        _app()
        with tempfile.TemporaryDirectory() as tmp:
            w = types.SimpleNamespace(_last_folder=tmp)
            calls, ask = _recording("")
            with _swap(QFileDialog, "getOpenFileName", ask), \
                    _swap(QFileDialog, "getSaveFileName", ask):
                assert get_open_file_name(w, "t", "*") == ("", "")
                assert get_save_file_name(w, "t", "*") == ("", "")
            assert w._last_folder == tmp
            assert len(calls) == 2

    def test_the_dialog_has_the_owner_it_is_given(self):
        from PySide6.QtWidgets import QFileDialog
        from ogr_ui.file_folders import get_open_file_name
        _app()
        w, owner = types.SimpleNamespace(), object()
        calls, ask = _recording()
        with _swap(QFileDialog, "getOpenFileName", ask):
            get_open_file_name(w, "t", "*", parent=owner)
        assert calls[0][0] is owner

    def test_save_proposes_its_name_inside_the_folder(self):
        from PySide6.QtWidgets import QFileDialog
        from ogr_ui.file_folders import get_save_file_name
        _app()
        with tempfile.TemporaryDirectory() as tmp:
            w = types.SimpleNamespace(_last_folder=tmp)
            calls, ask = _recording()
            with _swap(QFileDialog, "getSaveFileName", ask):
                get_save_file_name(w, "t", "*.pdf", "Demo_report.pdf")
                get_save_file_name(w, "t", "*.pdf")
            assert [c[2] for c in calls] == \
                [os.path.join(tmp, "Demo_report.pdf"), tmp], calls

    def test_save_remembers_the_folder_of_the_file(self):
        from PySide6.QtWidgets import QFileDialog
        from ogr_ui.file_folders import get_save_file_name
        _app()
        with tempfile.TemporaryDirectory() as tmp:
            w = types.SimpleNamespace()
            target = os.path.join(tmp, "informe.pdf")
            calls, ask = _recording(target)
            with _swap(QFileDialog, "getSaveFileName", ask):
                assert get_save_file_name(w, "t", "*.pdf")[0] == target
            assert _norm(w._last_folder) == _norm(tmp)
