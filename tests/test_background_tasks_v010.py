# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
v0.1.0 — a calculation handed to ``ogr_ui.background.run_task`` runs off
the window's thread, can be cancelled, reports at most one signal per
percent, leaves nothing of itself alive, and waits for a results file still
being written; and the progress dialog in front of it does not close before
the calculation has returned.

WHAT INVARIANT THIS PROTECTS, ported from OGR Slip2D (v0.1.486), where these
tests drove the main window and the limit-equilibrium engine. Here the
window is a bare ``QMainWindow`` or ``QWidget`` and the calculation a plain
Python function:

* ``tests/test_background_tasks_v1365.py`` (v0.1.365, D348; the Cancel of
  v0.1.366, D362): without a display the calculation runs inline and gets
  ``None`` as its callback; with ``window._tasks_threaded = True`` it runs
  on another thread while the window's event loop dispatches events, the
  ``TaskProgressDialog`` is the modal widget and ``window.task_worker`` is
  the thread; its result or its exception comes back to the caller; and the
  dialog does not close (Esc, the title bar) until the calculation returns.
  The engine's five calculations compared bit for bit through the thread
  stay in Slip2D: they are its numbers, not this module's;
* ``tests/test_task_progress_v1386.py`` (v0.1.386): one signal per percent
  of each (total, phase), the stop flag read on every call, a new phase or
  total always sent, and 1764 calls through the real door reach the dialog
  101 times;
* ``tests/test_task_frees_v1398.py`` (v0.1.398, D382): the worker does not
  keep the result or the exception, so what a cancelled, failed or
  successful calculation computed is freed without the cyclic collector.
  The case of a real Compute cancelled in its second method needs the
  engine and stays in Slip2D;
* the ``wait_for_results_file`` part of
  ``tests/test_results_file_first_v1405.py`` (v0.1.405, D390): a
  calculation starts only after the thread the window keeps as
  ``_results_writer`` has returned, with a dialog that says so; with no
  writer, no wait. ``ResultsWriter`` and ``write_results_file`` stayed in
  Slip2D, and so did their part.

What OGR GUI 0.1.0 changed, tested here: the checkpoints and the phase come
from ``install_progress(watching, phase, phase_texts)`` instead of
``ogr_core.progress`` (a fake ``watching`` context manager and ``phase``
function stand in for the core's); without them ``run_task`` still works
and the stop is still read on every progress call; ``reset_progress()``
forgets them; and ``TaskProgressDialog(phase_texts=...)`` shows the
program's text for a phase.

Every test puts back what it installs (``reset_progress``, the language, a
module attribute it replaces) in ``finally`` (rule 5).
"""
from __future__ import annotations

import contextlib
import gc
import threading
import weakref

import pytest


def _app():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


def _window(threaded=None, kind="main"):
    """A bare window; ``threaded`` sets ``_tasks_threaded`` when not None."""
    from PySide6.QtWidgets import QMainWindow, QWidget
    _app()
    w = QMainWindow() if kind == "main" else QWidget()
    if threaded is not None:
        w._tasks_threaded = threaded
    return w


def _done(w):
    w.close()
    w.deleteLater()


@contextlib.contextmanager
def _installed(watching=None, phase=None, phase_texts=None):
    """``install_progress`` for a block, forgotten on the way out."""
    from ogr_ui import background as bg
    bg.install_progress(watching, phase, phase_texts)
    try:
        yield
    finally:
        bg.reset_progress()


@contextlib.contextmanager
def _language(code):
    from ogr_ui.i18n import current_language, set_language
    before = current_language()
    set_language(code)
    try:
        yield
    finally:
        set_language(before)


@contextlib.contextmanager
def _dialogs(made):
    """Every ``TaskProgressDialog`` the block builds, appended to ``made``:
    ``run_task`` and ``wait_for_results_file`` import it from its module
    when they run, so a subclass put there is the one they build."""
    import ogr_ui.dialogs.progress_dialog as pd
    real = pd.TaskProgressDialog

    class Spy(real):
        def __init__(self, parent=None, title="", on_cancel=None,
                     phase_texts=None):
            super().__init__(parent, title, on_cancel,
                             phase_texts=phase_texts)
            made.append(self)
            self.updates = []

        def update_progress(self, done, total, phase=""):
            self.updates.append((done, total, phase))
            super().update_progress(done, total, phase)

    pd.TaskProgressDialog = Spy
    try:
        yield
    finally:
        pd.TaskProgressDialog = real


class _Handshake:
    """From inside the calculation, ask the window's thread to run
    ``on_main()`` and wait (up to 3 s) until it has. Only possible while the
    window's event loop runs: on the window's own thread the wait would time
    out (the measure of Slip2D's v0.1.365 test, which a timer was not)."""

    WAIT = 3.0

    def __init__(self, on_main):
        from PySide6.QtCore import QEvent, QObject
        self.done = threading.Event()
        outer = self

        class Probe(QObject):
            def event(self, ev):
                if ev.type() == QEvent.User:
                    on_main()
                    outer.done.set()
                    return True
                return super().event(ev)
        _app()
        self.probe = Probe()

    def __call__(self) -> bool:
        from PySide6.QtCore import QCoreApplication, QEvent
        QCoreApplication.postEvent(self.probe, QEvent(QEvent.User))
        return self.done.wait(self.WAIT)


# ======================================================================
class TestInline:
    """Without a display the calculation runs inline, as it always did."""

    def test_without_a_display_it_runs_inline(self):
        from PySide6.QtWidgets import QApplication

        from ogr_ui.background import run_task, runs_inline
        w = _window()
        try:
            offscreen = QApplication.instance().platformName() == "offscreen"
            assert runs_inline(w) is offscreen
            if offscreen:
                got = []
                assert run_task(w, lambda cb: got.append(cb) or 7) == 7
                assert got == [None], "inline, the callback is None"
                assert getattr(w, "task_worker", None) is None
        finally:
            _done(w)

    def test_the_window_can_force_either_way(self):
        from ogr_ui.background import runs_inline
        w = _window(threaded=True)
        try:
            assert not runs_inline(w)
            w._tasks_threaded = False
            assert runs_inline(w)
        finally:
            _done(w)

    def test_an_inline_error_reaches_the_caller(self):
        from ogr_ui.background import run_task
        w = _window(threaded=False)

        def fn(cb):
            raise ValueError("bad model")
        try:
            with pytest.raises(ValueError):
                run_task(w, fn)
        finally:
            _done(w)


# ======================================================================
class TestThroughTheThread:

    def test_the_window_runs_its_loop_while_it_computes(self):
        from PySide6.QtWidgets import QApplication

        from ogr_ui.background import _TaskWorker, run_task
        w = _window(threaded=True)
        seen = {}

        def on_main():
            m = QApplication.activeModalWidget()
            seen["modal"] = type(m).__name__ if m is not None else None
            seen["worker"] = type(getattr(w, "task_worker", None)).__name__
        shake = _Handshake(on_main)

        def fn(cb):
            seen["on_main"] = (threading.current_thread()
                               is threading.main_thread())
            seen["cb"] = cb is not None
            seen["answered"] = shake()
            return "returned"
        try:
            assert run_task(w, fn, "A task") == "returned"
            assert seen["on_main"] is False, "it ran on the window's thread"
            assert seen["cb"], "through the thread the callback is given"
            assert seen["answered"], \
                "the window dispatched no event while computing"
            assert seen["modal"] == "TaskProgressDialog", seen["modal"]
            assert seen["worker"] == _TaskWorker.__name__, \
                "the agent's bridge would let an edit through"
            assert w.task_worker is None
        finally:
            _done(w)

    def test_an_error_on_the_thread_reaches_the_caller(self):
        from ogr_ui.background import run_task
        w = _window(threaded=True, kind="widget")

        def fn(cb):
            raise ValueError("stop here")
        try:
            try:
                run_task(w, fn, "A task")
            except ValueError as exc:
                assert str(exc) == "stop here"
            else:
                raise AssertionError("the failure did not reach the caller")
            assert w.task_worker is None
        finally:
            _done(w)

    def test_cancel_raises_task_cancelled(self):
        from ogr_ui.background import TaskCancelled, run_task
        w = _window(threaded=True)
        calls = []

        def fn(cb):
            w.task_worker.stop.set()
            calls.append(1)
            cb(1, 2)                         # the stop is read here
            calls.append(2)
            return "published"
        try:
            with pytest.raises(TaskCancelled):
                run_task(w, fn, "A task")
            assert calls == [1], "the calculation went on after the stop"
            assert w.task_worker is None
        finally:
            _done(w)

    def test_task_cancelled_goes_through_except_exception(self):
        """A ``BaseException``: the engine's ``except Exception`` around a
        surface it cannot evaluate must not swallow the stop (D362)."""
        from ogr_ui.background import TaskCancelled
        assert not issubclass(TaskCancelled, Exception)
        assert issubclass(TaskCancelled, BaseException)

    def test_the_dialogs_cancel_stops_it_and_says_so(self):
        """The user's Cancel: the dialog asks the calculation to stop, says
        «Cancelling…», disables its button and stays until it returns."""
        from PySide6.QtWidgets import QApplication

        from ogr_ui.background import TaskCancelled, run_task
        from ogr_ui.i18n import tr
        w = _window(threaded=True)
        seen = {}

        def press_cancel():
            d = QApplication.activeModalWidget()
            d.reject()
            seen["text"] = d.lbl_status.text()
            seen["button"] = d.btn_cancel.isEnabled()
            seen["visible"] = not d.isHidden()
        shake = _Handshake(press_cancel)

        def fn(cb):
            cb(0, 10)
            assert shake(), "the window did not answer"
            for done in range(1, 11):
                cb(done, 10)
            return "published"
        try:
            with pytest.raises(TaskCancelled):
                run_task(w, fn, "A task")
            assert seen["text"] == tr("Cancelling...")
            assert seen["button"] is False
            assert seen["visible"], "Cancel closed it with the thread running"
        finally:
            _done(w)


# ======================================================================
class TestTheProgramsCheckpointsAndPhase:
    """``install_progress``: what ``ogr_core.progress`` gave in Slip2D."""

    def test_the_checkpoints_read_the_stop(self):
        """A loop that never calls back is stopped at its checkpoints:
        ``watching(check)`` is entered on the calculation's thread, and
        ``check()`` raises once Cancel is pressed."""
        from ogr_ui.background import TaskCancelled, run_task
        current = {}
        entered = []

        @contextlib.contextmanager
        def watching(check):
            entered.append(threading.current_thread()
                           is threading.main_thread())
            current["check"] = check
            try:
                yield
            finally:
                current.pop("check", None)
                entered.append("exited")

        w = _window(threaded=True)
        steps = []

        def fn(cb):
            for i in range(5):
                if i == 2:
                    w.task_worker.stop.set()
                current["check"]()           # the core's checkpoint
                steps.append(i)
            return "published"
        try:
            with _installed(watching=watching):
                with pytest.raises(TaskCancelled):
                    run_task(w, fn, "A task")
            assert steps == [0, 1]
            assert entered == [False, "exited"], entered
        finally:
            _done(w)

    def test_without_them_it_still_works(self):
        from ogr_ui import background as bg
        bg.reset_progress()
        assert bg._SOURCE == {}
        assert bg._phase() == ""
        with bg._watching(lambda: None):     # a null context
            pass
        w = _window(threaded=True)
        try:
            assert bg.run_task(w, lambda cb: (cb(1, 2), "ok")[1]) == "ok"
        finally:
            _done(w)

    def test_the_phase_goes_with_every_signal(self):
        from ogr_ui.background import _TaskWorker
        now = {"phase": ""}
        _app()
        with _installed(phase=lambda: now["phase"]):
            worker = _TaskWorker(lambda cb: None)
            got = []
            worker.progress.connect(lambda d, t, p: got.append((d, t, p)))
            worker._progress(10, 100)
            worker._progress(10, 100)        # the same: not sent
            worker._progress(20, 200)        # a new total: sent
            now["phase"] = "optimize"
            worker._progress(20, 200)        # a new phase: sent
        assert got == [(10, 100, ""), (20, 200, ""), (20, 200, "optimize")]

    def test_a_phase_of_none_is_no_phase(self):
        from ogr_ui import background as bg
        with _installed(phase=lambda: None):
            assert bg._phase() == ""

    def test_reset_forgets_what_was_installed(self):
        from ogr_ui import background as bg
        with _installed(watching=lambda check: contextlib.nullcontext(),
                        phase=lambda: "p", phase_texts={"p": "Pee"}):
            assert set(bg._SOURCE) == {"watching", "phase", "phase_texts"}
        assert bg._SOURCE == {}

    def test_install_replaces_what_was_there(self):
        """A second ``install_progress`` is the whole of it: a phase not
        given again is gone."""
        from ogr_ui import background as bg
        try:
            bg.install_progress(phase=lambda: "p")
            bg.install_progress(phase_texts={"p": "Pee"})
            assert set(bg._SOURCE) == {"phase_texts"}
            assert bg._phase() == ""
        finally:
            bg.reset_progress()

    def test_the_dialog_gets_the_programs_phase_texts(self):
        """Through the real door: the phase the program names reaches the
        dialog, which shows the program's text for it."""
        from ogr_ui.background import run_task
        now = {"phase": ""}
        texts = {"optimize": "Optimizing the critical surface..."}
        made = []
        w = _window(threaded=True)

        def fn(cb):
            cb(1, 4)
            now["phase"] = "optimize"
            cb(3, 4)
            return "ok"
        try:
            with _installed(phase=lambda: now["phase"], phase_texts=texts), \
                    _dialogs(made):
                assert run_task(w, fn, "A task") == "ok"
            assert len(made) == 1
            d = made[0]
            assert d.updates == [(1, 4, ""), (3, 4, "optimize")]
            assert d.lbl_status.text() == \
                "Optimizing the critical surface... 3/4"
        finally:
            _done(w)


# ======================================================================
class TestTheDialog:

    def test_it_does_not_close_before_the_calculation_returns(self):
        from ogr_ui.dialogs.progress_dialog import TaskProgressDialog
        _app()
        d = TaskProgressDialog(None, "x")
        try:
            d.show()
            d.reject()
            assert not d.isHidden(), "Esc closed it with the thread running"
            d.close()
            assert not d.isHidden(), "the title bar closed it"
            assert d.btn_cancel.isHidden(), "a Cancel that cancels nothing"
            assert d.bar.maximum() == 0, "busy until a total is known"
            d.update_progress(3, 10)
            assert d.bar.maximum() == 100 and d.bar.value() == 30
            d.finish()
            assert d.isHidden()
        finally:
            d._finished = True
            d.close()
            d.deleteLater()

    def test_its_cancel_asks_once(self):
        from ogr_ui.dialogs.progress_dialog import TaskProgressDialog
        _app()
        asked = []
        d = TaskProgressDialog(None, "x", on_cancel=lambda: asked.append(1))
        try:
            assert not d.btn_cancel.isHidden()
            d.reject()
            d.reject()
            assert asked == [1]
            assert d.cancelled
            # once cancelling, progress does not overwrite «Cancelling…»
            text = d.lbl_status.text()
            d.update_progress(5, 10)
            assert d.lbl_status.text() == text
        finally:
            d.finish()
            d.deleteLater()

    def test_a_phase_shows_the_programs_text_translated(self):
        from ogr_ui.dialogs.progress_dialog import TaskProgressDialog
        _app()
        d = TaskProgressDialog(None, "x", phase_texts={"p": "Computing...",
                                                       "q": "Gauging..."})
        try:
            with _language("es"):
                d.update_progress(3, 10, "p")
                assert d.lbl_status.text() == "Calculando... 3/10"
            d.update_progress(4, 10, "q")
            assert d.lbl_status.text() == "Gauging... 4/10"
            # a phase it has no text for: the default
            d.update_progress(5, 10, "unknown")
            assert d.lbl_status.text() == "Computing... 5/10"
            # no total: nothing to show a phase with
            d.update_progress(0, 0, "q")
            assert d.lbl_status.text() == "Computing... 5/10"
        finally:
            d.finish()
            d.deleteLater()

    def test_without_phase_texts_no_phase_is_named(self):
        from ogr_ui.dialogs.progress_dialog import TaskProgressDialog
        _app()
        d = TaskProgressDialog(None, "x")
        try:
            d.update_progress(2, 8, "optimize")
            assert d.lbl_status.text() == "Computing... 2/8"
        finally:
            d.finish()
            d.deleteLater()


# ======================================================================
def _worker():
    """A worker that is never started, and what its signal sends. Emitted
    on this thread, the signal reaches the recorder at once."""
    from ogr_ui.background import _TaskWorker
    _app()
    w = _TaskWorker(lambda cb: None)
    got = []
    w.progress.connect(lambda done, total, phase: got.append(
        (done, total, phase)))
    return w, got


class TestOneSignalPerPercent:
    """test_task_progress_v1386, invariants 1 to 4."""

    def test_a_run_of_442_calls_sends_101(self):
        w, got = _worker()
        for done in range(442):
            w._progress(done, 441)
        assert len(got) == 101
        assert [int(100 * d / t) for d, t, _ph in got] == list(range(101))
        assert got[0] == (0, 441, "")
        assert got[-1] == (441, 441, "")

    def test_the_stop_flag_is_read_on_every_call(self):
        from ogr_ui.background import TaskCancelled
        w, got = _worker()
        w._progress(5, 441)                       # 1 %: sent
        w.stop.set()
        with pytest.raises(TaskCancelled):
            w._progress(6, 441)                   # still 1 %: not sent, read
        assert len(got) == 1

    def test_a_run_without_a_total_is_sent_once(self):
        w, got = _worker()
        w._progress(0, 0)
        w._progress(0, 0)
        assert got == [(0, 0, "")]

    def test_run_task_on_its_thread(self):
        from ogr_ui.background import run_task
        made = []
        window = _window(threaded=True, kind="widget")

        def calculation(cb):
            for done in range(1, 1765):
                cb(done, 1764)
            return "returned"
        try:
            with _dialogs(made):
                assert run_task(window, calculation) == "returned"
            calls = made[0].updates
            assert len(calls) == 101
            assert calls[-1] == (1764, 1764, "")
        finally:
            _done(window)


# ======================================================================
class _Marker:
    """Something a calculation computed (weakly referenceable)."""


@contextlib.contextmanager
def _collector_off():
    was = gc.isenabled()
    gc.collect()
    gc.disable()
    try:
        yield
    finally:
        if was:
            gc.enable()


class TestNothingOutlivesItsTask:
    """test_task_frees_v1398: with automatic collection off between the
    calculation and the check, so no collection frees a cycle behind the
    test's back."""

    def test_a_cancelled_task(self):
        from ogr_ui.background import TaskCancelled, run_task
        w = _window(threaded=True, kind="widget")
        refs = []

        def fn(cb):
            computed = _Marker()
            refs.append(weakref.ref(computed))
            w.task_worker.stop.set()
            cb(1, 2)            # the window's check raises here
            return computed
        try:
            with _collector_off():
                try:
                    run_task(w, fn, "Compute")
                except TaskCancelled:
                    pass
                else:
                    raise AssertionError("the task was not cancelled")
                assert w.task_worker is None
                assert refs[0]() is None, (
                    "what the cancelled calculation computed is still alive")
        finally:
            _done(w)

    def test_a_failed_task(self):
        from ogr_ui.background import run_task
        w = _window(threaded=True, kind="widget")
        refs = []

        def fn(cb):
            computed = _Marker()
            refs.append(weakref.ref(computed))
            raise ValueError("bad model")
        try:
            with _collector_off():
                try:
                    run_task(w, fn, "Compute")
                except ValueError as exc:
                    assert str(exc) == "bad model"
                else:
                    raise AssertionError("the failure did not reach the "
                                         "caller")
                assert refs[0]() is None, (
                    "what the failed calculation computed is still alive")
        finally:
            _done(w)

    def test_a_successful_task(self):
        from ogr_ui.background import run_task
        w = _window(threaded=True, kind="widget")
        refs = []

        def fn(cb):
            computed = _Marker()
            refs.append(weakref.ref(computed))
            return computed
        try:
            with _collector_off():
                got = run_task(w, fn, "Compute")
                assert refs[0]() is got
                del got
                assert refs[0]() is None, "something kept the returned result"
        finally:
            _done(w)


# ======================================================================
def _writer(log, gate):
    """A results writer held by ``gate``: a thread the window keeps as
    ``_results_writer``, as Slip2D's ``ResultsWriter`` is."""
    from PySide6.QtCore import QThread

    class Writer(QThread):
        def run(self):
            gate.wait(10)
            log.append("file written")
    _app()
    return Writer()


class TestTheFileFirst:
    """test_results_file_first_v1405, the part that stayed here."""

    def test_a_calculation_waits_for_the_file(self):
        from ogr_ui.background import run_task
        from ogr_ui.i18n import tr
        w = _window(threaded=True)
        log, made, gate = [], [], threading.Event()
        writer = _writer(log, gate)
        release = threading.Timer(0.2, gate.set)
        try:
            w._results_writer = writer
            writer.start()
            assert writer.isRunning()
            with _dialogs(made):
                release.start()
                run_task(w, lambda cb: log.append("calculation"), "Compute")
            assert log == ["file written", "calculation"], log
            titles = [d.windowTitle() for d in made]
            assert titles == [tr("Saving the results file..."), "Compute"], \
                titles
            assert made[0].btn_cancel.isHidden(), "a wait with a Cancel"
        finally:
            gate.set()
            release.cancel()
            release.join()
            writer.wait()
            _done(w)

    def test_nothing_to_wait_for(self):
        from ogr_ui.background import run_task, wait_for_results_file
        w = _window(threaded=True)
        log, made = [], []
        try:
            wait_for_results_file(w)             # no writer at all
            with _dialogs(made):
                run_task(w, lambda cb: log.append("calculation"), "Compute")
            assert log == ["calculation"]
            assert [d.windowTitle() for d in made] == ["Compute"]
        finally:
            _done(w)

    def test_a_writer_that_has_finished_is_not_waited_for(self):
        from ogr_ui.background import wait_for_results_file
        log, made, gate = [], [], threading.Event()
        gate.set()
        writer = _writer(log, gate)
        w = _window(threaded=True)
        try:
            writer.start()
            writer.wait()
            w._results_writer = writer
            with _dialogs(made):
                wait_for_results_file(w)
            assert made == [], "a dialog for a file already written"
            assert log == ["file written"]
        finally:
            _done(w)
