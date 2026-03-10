import os
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QCursor

from ui.constants import TXT, TXT2, TXT3, PRI, PRI_L, OK, ERR, ERR_BG, WARN, ITEM_H
from ui.helpers import make_thumbnail, draw_rounded_pixmap, fmt_bytes


class FileItemWidget(QWidget):
    """One row in the file list showing thumbnail, name, size, status."""
    remove_requested = Signal(object)   # self

    _SPINNER = ["◐", "◓", "◑", "◒"]

    def __init__(self, row: int, file_path: str, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.row       = row
        self.file_path = file_path
        self._status   = "pending"   # pending | converting | ok | error
        self._err_msg  = ""
        self._spin_idx = 0
        self._spin_timer = QTimer(self)
        self._spin_timer.setInterval(120)
        self._spin_timer.timeout.connect(self._tick_spinner)

        self.setFixedHeight(72)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(
            "FileItemWidget { background: transparent; border-radius: 10px; }"
        )
        self._build()

    # ── Build layout ──────────────────────────────────────────────
    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(12)

        # Thumbnail
        thumb_pm = make_thumbnail(self.file_path, 52)
        thumb_pm = draw_rounded_pixmap(thumb_pm, 8)
        self.thumb_lbl = QLabel()
        self.thumb_lbl.setPixmap(thumb_pm)
        self.thumb_lbl.setFixedSize(52, 52)
        self.thumb_lbl.setStyleSheet("background: transparent;")

        # Info
        info = QWidget()
        info.setStyleSheet("background: transparent;")
        info_lay = QVBoxLayout(info)
        info_lay.setContentsMargins(0, 0, 0, 0)
        info_lay.setSpacing(3)

        name   = Path(self.file_path).name
        ext    = Path(self.file_path).suffix.lstrip(".").upper() or "FILE"
        try:
            size_b = os.path.getsize(self.file_path)
            size_s = fmt_bytes(size_b)
        except OSError:
            size_s = "—"

        # Row 1: filename
        self.name_lbl = QLabel(name)
        self.name_lbl.setStyleSheet(
            f"font-weight: 600; font-size: 13px; color:{TXT}; background:transparent;"
        )
        self.name_lbl.setMaximumWidth(340)
        # Elide long filenames
        fm = self.name_lbl.fontMetrics()
        self.name_lbl.setText(fm.elidedText(name, Qt.TextElideMode.ElideMiddle, 340))
        self.name_lbl.setToolTip(name)

        # Row 2: size + format badge
        meta_row = QWidget()
        meta_row.setStyleSheet("background: transparent;")
        meta_lay = QHBoxLayout(meta_row)
        meta_lay.setContentsMargins(0, 0, 0, 0)
        meta_lay.setSpacing(7)

        self.size_lbl = QLabel(size_s)
        self.size_lbl.setStyleSheet(
            f"font-size: 11px; color:{TXT2}; background:transparent;"
        )

        self.ext_badge = QLabel(ext)
        self.ext_badge.setStyleSheet(
            f"background:{PRI_L}; color:{PRI}; border-radius:5px;"
            f"padding:1px 7px; font-size:10px; font-weight:700;"
        )

        meta_lay.addWidget(self.size_lbl)
        meta_lay.addWidget(self.ext_badge)
        meta_lay.addStretch()

        info_lay.addWidget(self.name_lbl)
        info_lay.addWidget(meta_row)

        # Status indicator
        self.status_lbl = QLabel("•")
        self.status_lbl.setFixedWidth(60)
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setStyleSheet(
            f"font-size:12px; color:{TXT3}; background:transparent;"
        )

        # Remove button
        self.remove_btn = QPushButton("✕")
        self.remove_btn.setObjectName("remove")
        self.remove_btn.setFixedSize(26, 26)
        self.remove_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.remove_btn.setToolTip("Remove from list")
        self.remove_btn.clicked.connect(lambda: self.remove_requested.emit(self))

        lay.addWidget(self.thumb_lbl)
        lay.addWidget(info, stretch=1)
        lay.addWidget(self.status_lbl)
        lay.addWidget(self.remove_btn)

    # ── Hover highlight ────────────────────────────────────────────
    def enterEvent(self, _event):
        self.setStyleSheet(
            f"FileItemWidget {{ background:{ITEM_H}; border-radius:10px; }}"
        )

    def leaveEvent(self, _event):
        self.setStyleSheet(
            "FileItemWidget { background: transparent; border-radius: 10px; }"
        )

    # ── Status control ─────────────────────────────────────────────
    def set_status(self, status: str, msg: str = ""):
        self._status  = status
        self._err_msg = msg
        if status == "converting":
            self._spin_timer.start()
            self.remove_btn.setEnabled(False)
            self._set_status_label("⠿", WARN, "Converting…")
        else:
            self._spin_timer.stop()
            self.remove_btn.setEnabled(True)
            if status == "ok":
                self._set_status_label("✓", OK, f"Saved to:\n{msg}")
            elif status == "error":
                self._set_status_label("✗", ERR, msg)
            else:
                self._set_status_label("•", TXT3, "Ready")

    def _set_status_label(self, text: str, color: str, tooltip: str = ""):
        self.status_lbl.setText(text)
        self.status_lbl.setStyleSheet(
            f"font-size:14px; font-weight:700; color:{color}; background:transparent;"
        )
        if tooltip:
            self.status_lbl.setToolTip(tooltip)

    def _tick_spinner(self):
        self._spin_idx = (self._spin_idx + 1) % len(self._SPINNER)
        self._set_status_label(self._SPINNER[self._spin_idx], WARN)
