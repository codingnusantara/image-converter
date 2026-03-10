from pathlib import Path
from typing import List, Tuple, Optional

from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor

from ui.constants import TXT3
from ui.file_item import FileItemWidget


class FilesPanel(QFrame):
    """Scrollable list of FileItemWidget rows with a header bar."""
    count_changed = Signal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("card")
        self._items: List[FileItemWidget] = []
        self._paths: set = set()   # de-duplicate by resolved path
        self._build()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        h_lay = QHBoxLayout(header)
        h_lay.setContentsMargins(16, 14, 16, 10)
        h_lay.setSpacing(8)

        lbl = QLabel("FILES")
        lbl.setObjectName("section_lbl")

        self.badge = QLabel("0")
        self.badge.setObjectName("count_badge")

        h_lay.addWidget(lbl)
        h_lay.addWidget(self.badge)
        h_lay.addStretch()

        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.setObjectName("ghost")
        self.clear_btn.setFixedHeight(30)
        self.clear_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clear_btn.setEnabled(False)
        self.clear_btn.clicked.connect(self.clear_all)
        h_lay.addWidget(self.clear_btn)

        divider = QFrame()
        divider.setObjectName("divider")

        # Scroll area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.list_widget = QWidget()
        self.list_widget.setStyleSheet("background: transparent;")
        self.list_lay = QVBoxLayout(self.list_widget)
        self.list_lay.setContentsMargins(12, 8, 12, 12)
        self.list_lay.setSpacing(4)
        self.list_lay.addStretch()

        self.scroll.setWidget(self.list_widget)

        # Empty state
        self.empty_lbl = QLabel("No files added yet")
        self.empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_lbl.setStyleSheet(f"color:{TXT3}; font-size:13px; padding:30px;")

        outer.addWidget(header)
        outer.addWidget(divider)
        outer.addWidget(self.empty_lbl, stretch=1)
        outer.addWidget(self.scroll, stretch=1)
        self.scroll.hide()

    # ── Public API ─────────────────────────────────────────────────
    def add_files(self, paths: List[str]):
        added = 0
        for p in paths:
            resolved = str(Path(p).resolve())
            if resolved in self._paths:
                continue
            self._paths.add(resolved)
            item = FileItemWidget(len(self._items), p)
            item.remove_requested.connect(self._remove_item)
            # Insert before the trailing stretch
            self.list_lay.insertWidget(self.list_lay.count() - 1, item)
            self._items.append(item)
            added += 1
        if added:
            self._refresh_ui()

    def clear_all(self):
        for item in self._items:
            item.setParent(None)
            item.deleteLater()
        self._items.clear()
        self._paths.clear()
        self._refresh_ui()

    def reset_statuses(self):
        for item in self._items:
            item.set_status("pending")

    def get_tasks(self) -> List[Tuple[int, str]]:
        return [(item.row, item.file_path) for item in self._items]

    def get_item(self, row: int) -> Optional[FileItemWidget]:
        for item in self._items:
            if item.row == row:
                return item
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def is_converting(self) -> bool:
        return any(i._status == "converting" for i in self._items)

    # ── Internal ───────────────────────────────────────────────────
    def _remove_item(self, item: FileItemWidget):
        resolved = str(Path(item.file_path).resolve())
        self._paths.discard(resolved)
        self._items.remove(item)
        item.setParent(None)
        item.deleteLater()
        # Re-index rows
        for i, it in enumerate(self._items):
            it.row = i
        self._refresh_ui()

    def _refresh_ui(self):
        count = len(self._items)
        self.badge.setText(str(count))
        self.clear_btn.setEnabled(count > 0)
        if count == 0:
            self.scroll.hide()
            self.empty_lbl.show()
        else:
            self.empty_lbl.hide()
            self.scroll.show()
        self.count_changed.emit(count)
