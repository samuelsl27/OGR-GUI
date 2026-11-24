# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2026 Samuel Sáez López — Universidad Politécnica de Cartagena
"""
The progress of a calculation, in front of its window.

From OGR Slip2D's ``ogr_gui/dialogs/misc_dialogs.py`` (v0.1.486), where
both classes lived next to the About dialog of that program. Two changes on
the way out: the phase the dialog names came from ``ogr_core.progress``
(``OPTIMIZE``, «Optimizing the critical surface...») and is now the
program's, ``phase_texts``; and nothing here imports the core.

Author: Samuel Sáez López (UPCT)
"""
from __future__ import annotations

from typing import Mapping, Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QProgressBar, QPushButton, QVBoxLayout

from ogr_ui.i18n import tr


class ComputeProgressDialog(QDialog):
    """Modal progress dialog for a calculation that counts its steps."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("Computing..."))
        self.setMinimumWidth(360)
        layout = QVBoxLayout(self)

        self.lbl_status = QLabel(tr("Computing..."))
        layout.addWidget(self.lbl_status)

        self.bar = QProgressBar()
        self.bar.setRange(0, 100)
        layout.addWidget(self.bar)

        self.btn_cancel = QPushButton(tr("Cancel"))
        layout.addWidget(self.btn_cancel)
        self.btn_cancel.clicked.connect(self.reject)
        self.cancelled = False
        self.btn_cancel.clicked.connect(lambda: setattr(self, "cancelled", True))

    def update_progress(self, done: int, total: int) -> None:
        if total <= 0:
            return
        pct = int(100 * done / total)
        self.bar.setValue(pct)
        self.lbl_status.setText(f"{tr('Computing...')} {done}/{total}")


class TaskProgressDialog(ComputeProgressDialog):
    """The progress of a calculation that runs off the window's thread
    (OGR Slip2D v0.1.365, D348, :func:`ogr_ui.background.run_task`).

    Application-modal, so the model cannot be edited while another thread
    reads it, and it does NOT close until the calculation has returned: Esc
    and the title bar's button would otherwise hand the window back with the
    thread still running, which is how a Cancel let a recompute start on top
    of a running one (D362).

    Cancel, Esc and the title bar's button ask the calculation to stop
    (``on_cancel``) and the dialog says so and stays: it closes when the
    thread has returned, which a stopped calculation does at its next
    checkpoint (v0.1.366, D362).

    ``phase_texts`` maps a phase the calculation reports to the English text
    shown, translated, with its ``done/total``: over a second loop the bar
    starts again, and without its name that reads as the whole run starting
    again.
    """

    def __init__(self, parent=None, title: str = "", on_cancel=None,
                 phase_texts: Optional[Mapping[str, str]] = None) -> None:
        super().__init__(parent)
        if title:
            self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        # busy until a calculation that counts its steps says how many
        self.bar.setRange(0, 0)
        self._on_cancel = on_cancel
        self._phase_texts = dict(phase_texts or {})
        self.btn_cancel.setVisible(on_cancel is not None)
        self._finished = False

    def update_progress(self, done: int, total: int, phase: str = "") -> None:
        if self.cancelled:
            return
        if total > 0 and self.bar.maximum() == 0:
            self.bar.setRange(0, 100)
        super().update_progress(done, total)
        text = self._phase_texts.get(phase) if phase else None
        if text and total > 0:
            self.lbl_status.setText("%s %d/%d" % (tr(text), done, total))

    def finish(self) -> None:
        """Close it: the calculation has returned."""
        self._finished = True
        self.accept()

    def reject(self) -> None:          # Cancel, Esc, the title bar's button
        if self._finished:
            super().reject()
            return
        if self._on_cancel is not None and not self.cancelled:
            self.cancelled = True
            self._on_cancel()
            self.btn_cancel.setEnabled(False)
            self.lbl_status.setText(tr("Cancelling..."))

    def closeEvent(self, event) -> None:        # noqa: N802 - Qt's name
        if self._finished:
            super().closeEvent(event)
        else:
            event.ignore()
