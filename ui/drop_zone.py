import os
from pathlib import Path
from typing import List, Optional

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor, QPainter, QBrush, QPen, QColor, QDragEnterEvent, QDropEvent

from ui.constants import TXT, TXT3, BDR2, PRI, PRI_L, SUPPORTED_INPUTS


class DropZone(QWidget):
    """Large drag-and-drop chute + browse button."""
    files_dropped = Signal(list)   # list[str] of accepted file paths

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._hovered = False
        self.setAcceptDrops(True)
        self.setMinimumHeight(190)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._build()

    # ── Layout ────────────────────────────────────────────────────
    def _build(self):
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(10)
        lay.setContentsMargins(24, 20, 24, 20)

        # Emoji icon
        self.icon_lbl = QLabel("🖼️")
        self.icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        f = QFont()
        f.setPointSize(36)
        self.icon_lbl.setFont(f)
        self.icon_lbl.setStyleSheet("background: transparent;")

        # Headline
        self.head_lbl = QLabel("Drag & Drop images here")
        self.head_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fh = QFont()
        fh.setPointSize(14)
        fh.setWeight(QFont.Weight.DemiBold)
        self.head_lbl.setFont(fh)
        self.head_lbl.setStyleSheet(f"color:{TXT}; background:transparent;")

        # "or"
        self.or_lbl = QLabel("or")
        self.or_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.or_lbl.setStyleSheet(f"color:{TXT3}; background:transparent;")

        # Browse button
        self.browse_btn = QPushButton("  📁  Browse Files")
        self.browse_btn.setObjectName("browse")
        self.browse_btn.setFixedSize(180, 42)
        self.browse_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_btn.setToolTip("Select one or more image files")

        # Hint
        self.hint_lbl = QLabel(
            "Supports: HEIC · JPG · PNG · WEBP · BMP · GIF · TIFF · ICO"
        )
        self.hint_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_lbl.setStyleSheet(
            f"color:{TXT3}; font-size:11px; background:transparent;"
        )

        lay.addStretch()
        lay.addWidget(self.icon_lbl)
        lay.addWidget(self.head_lbl)
        lay.addWidget(self.or_lbl)
        lay.addWidget(self.browse_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.hint_lbl)
        lay.addStretch()

    # ── Paint ──────────────────────────────────────────────────────
    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(2, 2, -2, -2)
        radius = 16

        bg_col = QColor("#DDE3FF") if self._hovered else QColor(PRI_L)
        p.setBrush(QBrush(bg_col))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(r, radius, radius)

        pen = QPen(QColor(PRI if self._hovered else BDR2))
        pen.setWidth(2)
        pen.setStyle(Qt.PenStyle.DashLine)
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, radius, radius)

    # ── Drag / Drop ────────────────────────────────────────────────
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            self._hovered = True
            self.update()
            event.acceptProposedAction()

    def dragLeaveEvent(self, _event):
        self._hovered = False
        self.update()

    def dropEvent(self, event: QDropEvent):
        self._hovered = False
        self.update()
        paths = self._collect_paths(event.mimeData().urls())
        if paths:
            self.files_dropped.emit(paths)
        event.acceptProposedAction()

    @staticmethod
    def _collect_paths(urls) -> List[str]:
        result = []
        for url in urls:
            p = url.toLocalFile()
            if os.path.isdir(p):
                for child in Path(p).iterdir():
                    if child.suffix.lstrip(".").lower() in SUPPORTED_INPUTS:
                        result.append(str(child))
            elif Path(p).suffix.lstrip(".").lower() in SUPPORTED_INPUTS:
                result.append(p)
        return result
