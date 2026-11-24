# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
Qt objects found as garbage on a worker thread are freed on the main thread.

OGR Slip2D v0.1.302 (D310): the whole suite aborted about one run in two,
in ``Py_HandlePending -> BindingManager::runDeletionInMainThread ->
QObject::~QObject -> purecall -> abort``: the cyclic collector had run on a
process pool's thread, found Qt objects that earlier tests left as cyclic
garbage, and shiboken queued their deletion for the main thread.
``ogr_ui.gc_guard`` keeps a collection that starts off the main thread from
freeing anything, and holds what it found until ``release()`` lets a
collection on the main thread free it.

What this file protects:

* with the guard, a dialog in a reference cycle, collected on a worker
  thread, is NOT destroyed, not even after the main thread has run Python
  (when shiboken's pending calls run), until ``release()``, and then on the
  main thread;
* the control: without it, the worker's collection destroys the dialog on
  the worker thread itself, which Qt forbids for a widget;
* ``release()`` off the main thread does nothing, and on it returns how
  many objects it held; the collector's debug flags are as they were;
* ``install()`` is idempotent; the runner of this repository installs the
  guard (``tests/_runner.py``) and it is installed while these tests run.

From OGR Slip2D v0.1.486, ``tests/test_gc_guard_v1302.py`` (v0.1.302,
D310), without its two tests of the main window (its release timer and
that it installs the guard), which are Slip2D's.

The guard stays installed: the runner put it there. The control takes its
callback out for the length of one collection and puts it back; the
collector's switch is put back after every test (rule 5).
"""
from __future__ import annotations

import gc
import threading

from PySide6.QtCore import QObject, Slot
from PySide6.QtTest import QSignalSpy
from PySide6.QtWidgets import QApplication, QDialog


class _CyclicDialog(QDialog):
    pass


class _Watcher(QObject):
    """Lives on: records the thread its slot runs on. A slot of a living
    receiver runs directly when the signal is emitted on the receiver's
    thread, and is QUEUED when it is emitted on another one."""

    def __init__(self):
        super().__init__()
        self.threads = []

    @Slot()
    def hit(self):
        self.threads.append(threading.current_thread().name)


def _garbage_dialog(watcher):
    """A Python-owned dialog that only the cyclic collector can free; a spy
    counts its destruction (``destroyed`` is emitted by ~QObject)."""
    QApplication.instance() or QApplication([])
    d = _CyclicDialog()
    d.me = d
    d.destroyed.connect(watcher.hit)
    spy = QSignalSpy(d.destroyed)
    del d
    return spy


def _collect_on_a_worker():
    t = threading.Thread(target=gc.collect, name="worker")
    t.start()
    t.join()


def _main_thread_runs_python():
    """What gives queued Python pending calls (shiboken's deferred
    deletions) their turn: the main thread running bytecode."""
    for i in range(200000):
        _ = [i]


class _Collector:
    """The collector switched off for the test (no collection on the main
    thread may free the garbage first), and the guard installed; both as
    they were afterwards, and nothing left held."""

    def __enter__(self):
        from ogr_ui import gc_guard
        self.was_on = gc.isenabled()
        self.was_installed = gc_guard.installed()
        self.flags = gc.get_debug()
        gc_guard.install()
        gc.disable()
        return self

    def __exit__(self, *exc):
        from ogr_ui import gc_guard
        gc_guard.release()
        if not self.was_installed:
            gc_guard.uninstall()
        if self.was_on:
            gc.enable()
        return False


class TestTheGuard:
    def test_worker_garbage_waits_for_the_main_thread(self):
        from ogr_ui import gc_guard
        with _Collector() as c:
            watcher = _Watcher()
            spy = _garbage_dialog(watcher)
            _collect_on_a_worker()
            # No events processed here: a window left alive elsewhere could
            # free it (rightly, on this thread) before release() is called.
            _main_thread_runs_python()
            assert spy.count() == 0, "destroyed before the main thread let it"
            held = gc_guard.kept()
            assert held > 0
            # the worker's collection put the debug flags back
            assert gc.get_debug() == c.flags
            assert gc_guard.release() == held
            assert spy.count() == 1
            # destroyed on the main thread: the slot ran at once, directly
            assert watcher.threads == ["MainThread"], watcher.threads
            assert gc_guard.kept() == 0
            # nothing left to release
            assert gc_guard.release() == 0

    def test_without_it_the_worker_destroys_it(self):
        """The control: without the guard the worker thread's collection
        destroys the dialog THERE (Qt forbids destroying a widget off the
        GUI thread), and the receiver on the main thread only hears of it
        through a queued call."""
        from ogr_ui import gc_guard
        with _Collector():
            gc_guard.release()
            gc.callbacks.remove(gc_guard._callback)
            try:
                watcher = _Watcher()
                spy = _garbage_dialog(watcher)
                _collect_on_a_worker()
            finally:
                gc_guard.install()
            assert spy.count() == 1          # already destroyed...
            assert watcher.threads == []     # ...somewhere else: queued
            QApplication.processEvents()
            assert watcher.threads == ["MainThread"]
            assert gc_guard.kept() == 0

    def test_release_off_the_main_thread_does_nothing(self):
        from ogr_ui import gc_guard
        with _Collector():
            watcher = _Watcher()
            spy = _garbage_dialog(watcher)
            _collect_on_a_worker()
            held = gc_guard.kept()
            assert held > 0
            out = []
            t = threading.Thread(target=lambda: out.append(
                gc_guard.release()))
            t.start()
            t.join()
            assert out == [0] and gc_guard.kept() == held
            assert spy.count() == 0
            gc_guard.release()
            assert spy.count() == 1

    def test_a_collection_on_the_main_thread_frees_at_once(self):
        """The guard holds nothing a main-thread collection finds."""
        from ogr_ui import gc_guard
        with _Collector():
            watcher = _Watcher()
            spy = _garbage_dialog(watcher)
            gc.collect()
            assert spy.count() == 1
            assert watcher.threads == ["MainThread"]
            assert gc_guard.kept() == 0


class TestWhoInstallsIt:
    def test_install_is_idempotent(self):
        from ogr_ui import gc_guard
        with _Collector():
            gc_guard.install()
            gc_guard.install()
            assert gc.callbacks.count(gc_guard._callback) == 1

    def test_the_runner_installs_it(self):
        """``tests/_runner.py`` installs it before the run and releases
        before every file; here only that these tests run under it."""
        from ogr_ui import gc_guard
        assert gc_guard.installed()
