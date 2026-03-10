import os
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor, QPainter, QPainterPath, QImage

from ui.constants import PRI_L

register_heif_opener()


def fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} TB"


def make_thumbnail(path: str, size: int = 54) -> QPixmap:
    """Return a square thumbnail QPixmap; falls back to a placeholder."""
    placeholder = QPixmap(size, size)
    placeholder.fill(QColor(PRI_L))
    try:
        with Image.open(path) as img:
            img = img.copy()
            img.thumbnail((size * 3, size * 3), Image.LANCZOS)
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            raw = img.tobytes("raw", "RGBA")
            qi = QImage(
                raw, img.width, img.height,
                img.width * 4, QImage.Format.Format_RGBA8888
            ).copy()
            pm = QPixmap.fromImage(qi)
            # Centre-crop to a perfect square
            side = min(pm.width(), pm.height())
            x = (pm.width() - side) // 2
            y = (pm.height() - side) // 2
            pm = pm.copy(x, y, side, side)
            return pm.scaled(
                size, size,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
    except Exception:
        return placeholder


def draw_rounded_pixmap(pixmap: QPixmap, radius: int = 10) -> QPixmap:
    """Return a copy of pixmap with rounded corners."""
    result = QPixmap(pixmap.size())
    result.fill(Qt.GlobalColor.transparent)
    painter = QPainter(result)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    return result
