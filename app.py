#!/usr/bin/env python3
"""
Image Converter — A beautiful, cross-platform PySide6 image converter.
Supports: HEIC, JPEG, PNG, WEBP, BMP, GIF, TIFF, ICO, PDF
"""

import sys

try:
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import Qt
except ImportError:
    print("PySide6 is required. Run:  pip install PySide6")
    sys.exit(1)

from ui.constants import APP_NAME, APP_VERSION
from ui.main_window import MainWindow



# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setOrganizationName("ImageConverterPro")

    # High-DPI scaling is enabled by default in PySide6/Qt6.
    # The AA_UseHighDpiPixmaps attribute is deprecated.

    # Platform-specific font tuning
    if sys.platform == "darwin":      # macOS
        # Qt 6 automatically uses the correct system font (.AppleSystemUIFont / SF Pro)
        pass
    elif sys.platform == "win32":     # Windows — Segoe UI
        f = app.font()
        f.setFamily("Segoe UI")
        f.setPointSize(9)
        app.setFont(f)

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
