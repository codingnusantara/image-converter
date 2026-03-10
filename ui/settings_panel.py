from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSlider, QFileDialog,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

from ui.constants import OUTPUT_FORMATS, QUALITY_FMTS, PRI


class SettingsPanel(QFrame):
    """Right-side panel: format picker, quality slider, output folder."""
    settings_changed = Signal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setFixedWidth(270)
        self._output_folder: Optional[str] = None
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(18)

        # ── Format ──────────────────────────────────────
        lbl_fmt = QLabel("CONVERT TO")
        lbl_fmt.setObjectName("section_lbl")

        self.format_combo = QComboBox()
        self.format_combo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.format_combo.setToolTip("Choose the output format")
        for name, ext, desc in OUTPUT_FORMATS:
            self.format_combo.addItem(f"{name}  —  {desc}", ext)
        self.format_combo.currentIndexChanged.connect(self._on_format_change)

        # ── Quality ──────────────────────────────────────
        self.quality_box = QWidget()
        self.quality_box.setStyleSheet("background: transparent;")
        q_lay = QVBoxLayout(self.quality_box)
        q_lay.setContentsMargins(0, 0, 0, 0)
        q_lay.setSpacing(8)

        q_header = QHBoxLayout()
        lbl_q = QLabel("QUALITY")
        lbl_q.setObjectName("section_lbl")
        self.quality_val = QLabel("95%")
        self.quality_val.setStyleSheet(
            f"font-size:12px; font-weight:700; color:{PRI}; background:transparent;"
        )
        q_header.addWidget(lbl_q)
        q_header.addStretch()
        q_header.addWidget(self.quality_val)

        self.quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(95)
        self.quality_slider.setTickInterval(10)
        self.quality_slider.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.quality_slider.setToolTip("Higher = better quality, larger file")
        self.quality_slider.valueChanged.connect(
            lambda v: self.quality_val.setText(f"{v}%")
        )

        q_lay.addLayout(q_header)
        q_lay.addWidget(self.quality_slider)

        # ── Output Folder ────────────────────────────────
        lbl_out = QLabel("SAVE TO")
        lbl_out.setObjectName("section_lbl")

        self.folder_btn = QPushButton("📁  Same folder as input")
        self.folder_btn.setObjectName("folder_btn")
        self.folder_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.folder_btn.setToolTip(
            "Click to choose a custom output folder.\n"
            "By default, converted files are saved next to the originals."
        )
        self.folder_btn.clicked.connect(self._pick_folder)

        # ── Assemble ─────────────────────────────────────
        lay.addWidget(lbl_fmt)
        lay.addWidget(self.format_combo)
        lay.addWidget(self.quality_box)

        div = QFrame()
        div.setObjectName("divider")
        lay.addWidget(div)

        lay.addWidget(lbl_out)
        lay.addWidget(self.folder_btn)
        lay.addStretch()

        self._on_format_change()

    # ── Slots ──────────────────────────────────────────────────────
    def _on_format_change(self):
        ext = self.current_ext()
        self.quality_box.setVisible(ext in QUALITY_FMTS)

    def _pick_folder(self):
        path = QFileDialog.getExistingDirectory(
            self, "Choose Output Folder",
            self._output_folder or str(Path.home()),
        )
        if path:
            self._output_folder = path
            short = Path(path).name or path
            self.folder_btn.setText(f"📁  {short}")
            self.folder_btn.setToolTip(path)
        else:
            self._output_folder = None
            self.folder_btn.setText("📁  Same folder as input")
            self.folder_btn.setToolTip(
                "Click to choose a custom output folder.\n"
                "By default, files are saved next to the originals."
            )

    # ── Accessors ──────────────────────────────────────────────────
    def current_ext(self) -> str:
        return self.format_combo.currentData() or "jpg"

    def current_quality(self) -> int:
        return self.quality_slider.value()

    def output_folder(self) -> Optional[str]:
        return self._output_folder
