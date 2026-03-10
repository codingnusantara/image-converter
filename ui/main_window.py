import os
import sys
from pathlib import Path
from typing import List, Optional

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QFileDialog, QMessageBox,
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QFont, QCursor

from ui.constants import APP_NAME, MIN_W, MIN_H, DEF_W, DEF_H, TXT3, SUPPORTED_INPUTS
from ui.stylesheet import _build_stylesheet
from ui.worker import ConversionWorker
from ui.drop_zone import DropZone
from ui.files_panel import FilesPanel
from ui.settings_panel import SettingsPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._worker: Optional[ConversionWorker] = None
        self._last_out_folder: Optional[str] = None

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(MIN_W, MIN_H)
        self.resize(DEF_W, DEF_H)
        self.setStyleSheet(_build_stylesheet())
        self._build_ui()

    # ═══════════════════════════════════════════════════════════════
    # UI CONSTRUCTION
    # ═══════════════════════════════════════════════════════════════

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("page")
        self.setCentralWidget(root)

        main = QVBoxLayout(root)
        main.setContentsMargins(24, 22, 24, 22)
        main.setSpacing(18)

        # ── Header ──────────────────────────────────────────────────
        header = self._build_header()
        main.addWidget(header)

        # ── Drop Zone ───────────────────────────────────────────────
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self._on_files_added)
        self.drop_zone.browse_btn.clicked.connect(self._browse_files)
        main.addWidget(self.drop_zone)

        # ── Content Row (file list + settings) ──────────────────────
        content = QHBoxLayout()
        content.setSpacing(16)

        self.files_panel = FilesPanel()
        self.files_panel.count_changed.connect(self._on_count_changed)

        self.settings_panel = SettingsPanel()

        content.addWidget(self.files_panel, stretch=1)
        content.addWidget(self.settings_panel)
        main.addLayout(content, stretch=1)

        # ── Footer ──────────────────────────────────────────────────
        footer = self._build_footer()
        main.addWidget(footer)

    def _build_header(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background: transparent;")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(4, 0, 4, 0)
        lay.setSpacing(12)

        # Logo emoji + text
        logo = QLabel("🎨")
        logo_f = QFont()
        logo_f.setPointSize(28)
        logo.setFont(logo_f)
        logo.setStyleSheet("background: transparent;")

        text_col = QWidget()
        text_col.setStyleSheet("background: transparent;")
        tc_lay = QVBoxLayout(text_col)
        tc_lay.setContentsMargins(0, 0, 0, 0)
        tc_lay.setSpacing(2)

        title = QLabel(APP_NAME)
        title.setObjectName("title")
        subtitle = QLabel(
            "Convert any image format instantly — drag, drop, done."
        )
        subtitle.setObjectName("subtitle")

        tc_lay.addWidget(title)
        tc_lay.addWidget(subtitle)

        lay.addWidget(logo)
        lay.addWidget(text_col)
        lay.addStretch()

        # Shortcut hint
        hint = QLabel("Ctrl+O  browse · Ctrl+↵  convert")
        hint.setStyleSheet(
            f"color:{TXT3}; font-size:11px; background:transparent;"
        )
        lay.addWidget(hint)

        return w

    def _build_footer(self) -> QFrame:
        footer = QFrame()
        footer.setObjectName("card2")
        footer.setFixedHeight(88)

        lay = QHBoxLayout(footer)
        lay.setContentsMargins(20, 14, 20, 14)
        lay.setSpacing(14)

        # Progress section
        prog_col = QWidget()
        prog_col.setStyleSheet("background: transparent;")
        prog_lay = QVBoxLayout(prog_col)
        prog_lay.setContentsMargins(0, 0, 0, 0)
        prog_lay.setSpacing(6)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)

        self.status_lbl = QLabel("Add images to get started")
        self.status_lbl.setObjectName("stat_lbl")

        prog_lay.addWidget(self.progress_bar)
        prog_lay.addWidget(self.status_lbl)

        # Result labels (hidden until conversion done)
        self.result_ok_lbl  = QLabel("")
        self.result_ok_lbl.setObjectName("result_ok")
        self.result_ok_lbl.hide()
        self.result_err_lbl = QLabel("")
        self.result_err_lbl.setObjectName("result_err")
        self.result_err_lbl.hide()

        prog_lay.addWidget(self.result_ok_lbl)
        prog_lay.addWidget(self.result_err_lbl)

        # Open folder button (hidden until done)
        self.open_btn = QPushButton("📂  Open Folder")
        self.open_btn.setObjectName("ghost")
        self.open_btn.setFixedHeight(42)
        self.open_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.open_btn.setToolTip("Open the output folder in Finder / Explorer")
        self.open_btn.clicked.connect(self._open_output_folder)
        self.open_btn.hide()

        # Convert / Cancel button
        self.convert_btn = QPushButton("  Convert Now  ▶")
        self.convert_btn.setObjectName("primary")
        self.convert_btn.setFixedHeight(48)
        self.convert_btn.setMinimumWidth(180)
        self.convert_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.convert_btn.setToolTip("Start converting all listed images (Ctrl+Enter)")
        self.convert_btn.setEnabled(False)
        self.convert_btn.clicked.connect(self._on_convert_clicked)

        lay.addWidget(prog_col, stretch=1)
        lay.addWidget(self.open_btn)
        lay.addWidget(self.convert_btn)

        return footer

    # ═══════════════════════════════════════════════════════════════
    # KEYBOARD SHORTCUTS
    # ═══════════════════════════════════════════════════════════════

    def keyPressEvent(self, event):
        key   = event.key()
        mods  = event.modifiers()
        ctrl  = Qt.KeyboardModifier.ControlModifier
        enter = Qt.Key.Key_Return

        if mods & ctrl and key == Qt.Key.Key_O:
            self._browse_files()
        elif mods & ctrl and key in (enter, Qt.Key.Key_Enter):
            if self.convert_btn.isEnabled():
                self._on_convert_clicked()
        elif key == Qt.Key.Key_Escape and self._worker and self._worker.isRunning():
            self._cancel_conversion()
        else:
            super().keyPressEvent(event)

    # ═══════════════════════════════════════════════════════════════
    # FILE MANAGEMENT
    # ═══════════════════════════════════════════════════════════════

    def _browse_files(self):
        exts = " ".join(f"*.{e}" for e in sorted(SUPPORTED_INPUTS))
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            str(Path.home()),
            f"Images ({exts});;All Files (*)",
        )
        if paths:
            self._on_files_added(paths)

    def _on_files_added(self, paths: List[str]):
        self.files_panel.add_files(paths)

    def _on_count_changed(self, count: int):
        has = count > 0
        self.convert_btn.setEnabled(has)
        if has:
            self.status_lbl.setText(
                f"{count} file{'s' if count>1 else ''} ready to convert"
            )
        else:
            self.status_lbl.setText("Add images to get started")
            self.progress_bar.setValue(0)
            self.result_ok_lbl.hide()
            self.result_err_lbl.hide()
            self.open_btn.hide()

    # ═══════════════════════════════════════════════════════════════
    # CONVERSION
    # ═══════════════════════════════════════════════════════════════

    def _on_convert_clicked(self):
        if self._worker and self._worker.isRunning():
            self._cancel_conversion()
        else:
            self._start_conversion()

    def _start_conversion(self):
        tasks = self.files_panel.get_tasks()
        if not tasks:
            return

        ext     = self.settings_panel.current_ext()
        quality = self.settings_panel.current_quality()
        out_dir = self.settings_panel.output_folder()

        # Validate custom output folder is writable
        if out_dir and not os.access(out_dir, os.W_OK):
            QMessageBox.warning(
                self, "Permission Error",
                f"Cannot write to:\n{out_dir}\n\nPlease choose a different folder.",
            )
            return

        self.files_panel.reset_statuses()
        self.progress_bar.setValue(0)
        self.result_ok_lbl.hide()
        self.result_err_lbl.hide()
        self.open_btn.hide()
        self.convert_btn.setText("  ■  Cancel")
        self.convert_btn.setObjectName("ghost")
        self.convert_btn.setStyle(self.convert_btn.style())  # force re-polish

        self._total = len(tasks)
        self._done  = 0

        self._worker = ConversionWorker(tasks, ext, out_dir, quality)
        self._worker.file_started.connect(self._on_file_started)
        self._worker.file_done.connect(self._on_file_done)
        self._worker.all_done.connect(self._on_all_done)
        self._worker.start()

        self.status_lbl.setText(f"Converting 0 / {self._total}…")

    def _cancel_conversion(self):
        if self._worker:
            self._worker.abort()
        self.status_lbl.setText("Cancelling…")

    def _on_file_started(self, idx: int):
        item = self.files_panel.get_item(idx)
        if item:
            item.set_status("converting")

    def _on_file_done(self, idx: int, success: bool, msg: str):
        self._done += 1
        item = self.files_panel.get_item(idx)
        if item:
            item.set_status("ok" if success else "error", msg)

        pct = int(self._done / max(self._total, 1) * 100)
        self.progress_bar.setValue(pct)
        self.status_lbl.setText(f"Converting {self._done} / {self._total}…")

        # Remember a valid output folder for the "Open Folder" button
        if success and msg:
            self._last_out_folder = str(Path(msg).parent)

    def _on_all_done(self, converted: int, failed: int):
        self.progress_bar.setValue(100)

        self.convert_btn.setText("  Convert Now  ▶")
        self.convert_btn.setObjectName("primary")
        self.convert_btn.setStyle(self.convert_btn.style())

        if converted:
            self.result_ok_lbl.setText(f"✓  {converted} file{'s' if converted>1 else ''} converted")
            self.result_ok_lbl.show()
        if failed:
            self.result_err_lbl.setText(f"✗  {failed} failed — hover the ✗ icon for details")
            self.result_err_lbl.show()
        if not converted and not failed:
            self.status_lbl.setText("Cancelled")
        else:
            self.status_lbl.setText("Done!")

        if self._last_out_folder:
            self.open_btn.show()

    # ═══════════════════════════════════════════════════════════════
    # OPEN OUTPUT FOLDER
    # ═══════════════════════════════════════════════════════════════

    def _open_output_folder(self):
        folder = self._last_out_folder
        if not folder or not os.path.isdir(folder):
            return
        url = QUrl.fromLocalFile(folder)
        from PySide6.QtGui import QDesktopServices
        QDesktopServices.openUrl(url)

    # ═══════════════════════════════════════════════════════════════
    # CLOSE GUARD
    # ═══════════════════════════════════════════════════════════════

    def closeEvent(self, event):
        if self._worker and self._worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Conversion in progress",
                "A conversion is still running. Quit anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self._worker.abort()
                self._worker.wait(2000)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
