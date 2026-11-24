# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
Long calculations off the window's thread (v0.1.365, D348), and stopped when
the user cancels them (v0.1.366, D362).

*Compute* has run on its own thread since its first version, and the
drawdown sweep since v0.1.70, whose comment already said why: on a real model
a calculation on the window's thread leaves the window "simply not
responding for minutes". Compute Statistics, Compute Groundwater (steady and
transient), the back analysis and Optimize Surfaces still ran there. The
fifth interface test (0.1.355) measured it: a two-stage transient with
factors held the window for about seven minutes and the statistics for about
forty seconds, while Windows painted a dark window over it and the agent's
calls timed out.

:func:`run_task` keeps the handlers as they were — it RETURNS the result, so
the code after the calculation, the undo step around it included, reads
exactly as before — and keeps the window's event loop running meanwhile: the
calculation runs on a ``QThread`` and the window waits in a local event loop
with a modal progress dialog in front. The modal dialog is what keeps the
model still: the user cannot edit it while it is being read on another
thread.

**Cancel (v0.1.366, D362).** *Compute*'s Cancel closed its dialog and set a
flag nobody read: the thread went on, published its result over a model the
user could by then have edited, and a second Compute started on top of it
aborted the process when the first thread lost its last reference. Now the
button asks the calculation to stop, the dialog says "Cancelling…" and
stays until the thread has returned, and :class:`TaskCancelled` reaches the
handler, which publishes nothing. The stop is raised from the progress
callback the calculation already calls, and from the checkpoints of
``ogr_core.progress`` in the loops that have none: no signature of the
engine changes, and a run that is not cancelled computes what it always did.

Without a display (the tests, which build real windows on the "offscreen"
platform, and the bank's checks) the calculation runs inline, as it always
did: the fifty-odd tests that call these handlers and read the result on the
next line keep working unchanged, and a modal dialog is never opened where
nobody can close it. ``window._tasks_threaded = True`` forces the thread, for
the tests of this module.

**OGR GUI 0.1.0 — what changed on the way out of OGR Slip2D.** The
checkpoints and the phase came from ``ogr_core.progress``; this package
does not import the core, so a program hands them over once with
:func:`install_progress` (OGR Slip2D would pass
``ogr_core.progress.watching`` and ``ogr_core.progress.phase``). Without
them the stop is still read on every progress call, and no phase is shown.
The progress dialog came from Slip2D's ``misc_dialogs`` and is now
:mod:`ogr_ui.dialogs.progress_dialog`; the text it shows for a phase is
the program's (``phase_texts``). The results-file writer
(``ResultsWriter``, ``write_results_file``) stays in Slip2D: it writes the
core's ``Project`` results. :func:`wait_for_results_file` stays here: it
waits for whatever thread the window keeps as ``_results_writer``.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

import contextlib
import threading
from typing import Callable, Mapping, Optional


#: What :func:`install_progress` was given: the program's checkpoints and
#: phase, and the text of each phase. Module state on purpose: there is one
#: program in the process. Tests that install put it back with
#: :func:`reset_progress` (rule 5).
_SOURCE: dict = {}


def install_progress(watching: Optional[Callable] = None,
                     phase: Optional[Callable[[], str]] = None,
                     phase_texts: Optional[Mapping[str, str]] = None) -> None:
    """Where the calculations of this program report from.

    ``watching(check)`` is a context manager under which the program's
    loops call ``check()`` at their checkpoints; ``phase()`` names the
    phase the calculation is in; ``phase_texts`` maps a phase to the
    English text the dialog shows (translated with ``tr()``) with its
    ``done/total``."""
    _SOURCE.clear()
    if watching is not None:
        _SOURCE["watching"] = watching
    if phase is not None:
        _SOURCE["phase"] = phase
    if phase_texts:
        _SOURCE["phase_texts"] = dict(phase_texts)


def reset_progress() -> None:
    """Forget what :func:`install_progress` was given."""
    _SOURCE.clear()


def _watching(check):
    watching = _SOURCE.get("watching")
    return watching(check) if watching is not None else contextlib.nullcontext()


def _phase() -> str:
    phase = _SOURCE.get("phase")
    return (phase() or "") if phase is not None else ""

from PySide6.QtCore import QEventLoop, QThread, Signal
from PySide6.QtWidgets import QApplication


class TaskCancelled(BaseException):
    """The user cancelled the calculation (v0.1.366, D362).

    A ``BaseException`` on purpose, as ``KeyboardInterrupt`` is: the engine
    catches ``Exception`` around a surface it cannot evaluate, a search that
    fails, a pool that cannot start — and a stop must go through all of
    them, not be counted as one more failed surface."""


class _TaskWorker(QThread):
    """Runs ``fn(progress_cb)`` and keeps what it returned or raised."""

    progress = Signal(int, int, str)

    def __init__(self, fn: Callable) -> None:
        super().__init__()
        self._fn = fn
        self.result = None
        self.error: Optional[BaseException] = None
        #: Set by the window's Cancel; read by the calculation's thread.
        self.stop = threading.Event()
        #: The (percent, total, phase) the dialog was last sent.
        self._last_sent = None

    def run(self) -> None:                       # noqa: D102
        try:
            with _watching(self._check):
                self.result = self._fn(self._progress)
        except BaseException as exc:  # noqa: BLE001 - raised again in the window
            self.error = exc

    def _check(self) -> None:
        if self.stop.is_set():
            raise TaskCancelled()

    def _progress(self, done, total) -> None:
        self._check()
        now = _phase()
        # v0.1.386 — one signal per percent, not one per call. A Grid Search
        # run in-process calls back once per centre, and every signal queues
        # a Python slot on the window's thread, which has to win the GIL back
        # from this one: on a focused grid of 200 x 200 centres the window
        # froze for up to 7 s, and a Cancel was read after the run had ended,
        # so its result was published. The dialog shows a percentage, and a
        # done/total nobody reads at that rate; the stop flag above is still
        # read on every call.
        sent = (int(100 * done / total) if total > 0 else None,
                int(total), now)
        if sent == self._last_sent:
            return
        self._last_sent = sent
        self.progress.emit(int(done), int(total), now)


def runs_inline(window) -> bool:
    """Whether ``window`` computes on its own thread: without a display,
    unless ``window._tasks_threaded`` says otherwise."""
    forced = getattr(window, "_tasks_threaded", None)
    if forced is not None:
        return not forced
    app = QApplication.instance()
    return app is None or app.platformName() == "offscreen"


def run_task(window, fn: Callable, title: str = ""):
    """``fn(progress_cb)``, computed off the window's thread; its result, or
    its exception raised again here — :class:`TaskCancelled` when the user
    cancelled it.

    ``progress_cb`` is ``(done, total)`` for the progress dialog, or None
    when the calculation runs inline — which is the call the window made
    before, argument for argument. While it runs, ``window.task_worker`` is
    the thread, so the agent's bridge answers Busy to an edit.
    """
    if runs_inline(window):
        return fn(None)
    from ogr_ui.dialogs.progress_dialog import TaskProgressDialog

    # v0.1.405 (D390) — a results file still being written comes first
    wait_for_results_file(window)
    worker = _TaskWorker(fn)
    prog = TaskProgressDialog(window, title, on_cancel=worker.stop.set,
                              phase_texts=_SOURCE.get("phase_texts"))
    worker.progress.connect(prog.update_progress)
    loop = QEventLoop()
    # Queued to this thread: the loop quits when the calculation has
    # returned, whatever it returned, and a signal emitted before exec()
    # waits for it.
    worker.finished.connect(loop.quit)
    window.task_worker = worker
    try:
        worker.start()
        prog.show()
        loop.exec()
        # The thread keeps its last reference until it has returned: a
        # QThread destroyed while it runs aborts the process (D362).
        worker.wait()
    finally:
        prog.finish()
        window.task_worker = None
    # v0.1.398 (D382) — taken out of the worker, and raised from a local
    # cleared on the way out, as ``concurrent.futures.Future.result`` does.
    # The traceback holds the frames of the calculation, and they hold what
    # it had computed; it also holds the frame of ``run`` and this one, both
    # with the worker, and the worker held the exception: a cycle that only
    # the cyclic collector frees, and an idle window never runs a full
    # collection. A cancelled Compute kept its partial result (3.3 GB in the
    # interface test of 0.1.397) until the next calculation.
    error, worker.error = worker.error, None
    result, worker.result = worker.result, None
    if error is not None:
        try:
            raise error
        finally:
            error = None
    return result


def wait_for_results_file(window) -> None:
    """Before a calculation starts, wait for the results file of the last
    Compute if it is still being written (v0.1.405, D390).

    The writer of D385 (``ResultsWriter``) shares the interpreter with the
    calculation's thread, and makes tens of thousands of short calls into
    HDF5, each one waiting for its turn back: measured on the Bishop result
    of ACADS 1(a) at 25 x 25 x 12, 24.6 s alone and 122.3 s with a serial
    Compute running (``_auditoria/P8_interfaz/h5_escritor_concurrente.py``).
    The interface test of 0.1.402 chained calculations for six minutes after
    a Compute and its file never appeared meanwhile. Before 0.1.400 the file
    was always written before the next calculation; it is again, and the
    wait is what the writer had left, alone.

    A window-modal dialog with a busy bar and no Cancel, in a local event
    loop: the window stays responsive, and the model cannot be edited
    meanwhile. With no writer running it does nothing."""
    writer = getattr(window, "_results_writer", None)
    if writer is None:
        return
    from ogr_ui.dialogs.progress_dialog import TaskProgressDialog
    from ogr_ui.i18n import tr
    loop = QEventLoop()
    # connected BEFORE asking whether it runs: a ``finished`` emitted in
    # between is queued to this thread and quits the loop once it starts
    writer.finished.connect(loop.quit)
    try:
        if not writer.isRunning():
            return
        prog = TaskProgressDialog(window, tr("Saving the results file..."))
        try:
            prog.show()
            loop.exec()
            writer.wait()
        finally:
            prog.finish()
    finally:
        writer.finished.disconnect(loop.quit)
