from ui.constants import (
    BG, CARD, CARD2, BDR, BDR2,
    PRI, PRI_H, PRI_A, PRI_L, PRI_T,
    TXT, TXT2, TXT3,
    OK, ERR, ERR_BG,
)


def _build_stylesheet() -> str:
    return f"""
    /* ── Root ─────────────────────────── */
    QMainWindow, QWidget#page {{
        background: {BG};
    }}
    QWidget {{
        font-size: 13px;
        color: {TXT};
    }}
    QToolTip {{
        background: {TXT};
        color: {PRI_T};
        border: none;
        border-radius: 6px;
        padding: 5px 10px;
        font-size: 12px;
    }}

    /* ── Scroll ────────────────────────── */
    QScrollArea, QAbstractScrollArea,
    QScrollArea > QWidget > QWidget {{
        background: transparent;
        border: none;
    }}
    QScrollBar:vertical {{
        background: {BG};
        width: 8px;
        margin: 2px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background: {BDR2};
        min-height: 28px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical:hover  {{ background: {PRI}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{ background: none; }}

    /* ── Cards ─────────────────────────── */
    QFrame#card {{
        background: {CARD};
        border-radius: 14px;
        border: 1px solid {BDR};
    }}
    QFrame#card2 {{
        background: {CARD2};
        border-radius: 10px;
        border: 1px solid {BDR};
    }}
    QFrame#divider {{
        background: {BDR};
        max-height: 1px;
        min-height: 1px;
        border: none;
    }}

    /* ── Buttons ───────────────────────── */
    QPushButton {{
        background: {CARD};
        color: {TXT};
        border: 1.5px solid {BDR};
        border-radius: 8px;
        padding: 8px 18px;
        font-size: 13px;
    }}
    QPushButton:hover   {{ background: {CARD2}; border-color: {BDR2}; }}
    QPushButton:pressed {{ background: {PRI_L}; border-color: {PRI};  }}
    QPushButton:disabled {{
        color: {TXT3};
        background: {CARD2};
        border-color: {BDR};
    }}

    QPushButton#primary {{
        background: {PRI};
        color: {PRI_T};
        border: none;
        border-radius: 10px;
        padding: 13px 36px;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton#primary:hover   {{ background: {PRI_H}; }}
    QPushButton#primary:pressed {{ background: {PRI_A}; }}
    QPushButton#primary:disabled {{
        background: {BDR};
        color: {TXT3};
    }}

    QPushButton#ghost {{
        background: transparent;
        border: 1.5px solid {BDR};
        color: {TXT2};
        border-radius: 8px;
        padding: 8px 18px;
    }}
    QPushButton#ghost:hover   {{ background: {CARD2}; border-color: {BDR2}; }}
    QPushButton#ghost:pressed {{ background: {PRI_L}; }}
    QPushButton#ghost:disabled {{ color: {TXT3}; }}

    QPushButton#browse {{
        background: {PRI_L};
        color: {PRI};
        border: 2px solid {PRI};
        border-radius: 9px;
        padding: 10px 28px;
        font-size: 13px;
        font-weight: 600;
    }}
    QPushButton#browse:hover   {{ background: {PRI}; color: {PRI_T}; }}
    QPushButton#browse:pressed {{ background: {PRI_H}; color: {PRI_T}; }}

    QPushButton#remove {{
        background: transparent;
        border: none;
        color: {TXT3};
        font-size: 15px;
        padding: 0;
        border-radius: 6px;
        min-width: 24px; max-width: 24px;
        min-height: 24px; max-height: 24px;
    }}
    QPushButton#remove:hover {{
        background: {ERR_BG};
        color: {ERR};
    }}

    QPushButton#folder_btn {{
        background: {CARD2};
        color: {TXT2};
        border: 1.5px solid {BDR};
        border-radius: 8px;
        padding: 9px 12px;
        font-size: 12px;
        text-align: left;
    }}
    QPushButton#folder_btn:hover {{
        background: {CARD};
        border-color: {PRI};
        color: {PRI};
    }}

    /* ── ComboBox ──────────────────────── */
    QComboBox {{
        background: {CARD};
        border: 1.5px solid {BDR};
        border-radius: 9px;
        padding: 9px 14px;
        font-size: 13px;
        color: {TXT};
        min-height: 38px;
        selection-background-color: transparent;
    }}
    QComboBox:hover {{ border-color: {BDR2}; }}
    QComboBox:focus {{ border-color: {PRI};  }}
    QComboBox::drop-down {{
        border: none;
        width: 30px;
        subcontrol-position: right center;
    }}
    QComboBox::down-arrow {{
        image: none;
        width: 0; height: 0;
    }}
    QComboBox QAbstractItemView {{
        background: {CARD};
        border: 1.5px solid {BDR2};
        border-radius: 10px;
        selection-background-color: {PRI_L};
        selection-color: {PRI};
        outline: none;
        padding: 4px;
    }}
    QComboBox QAbstractItemView::item {{
        min-height: 34px;
        padding: 4px 14px;
        border-radius: 6px;
    }}
    QComboBox QAbstractItemView::item:hover {{
        background: {PRI_L};
        color: {PRI};
    }}

    /* ── Slider ────────────────────────── */
    QSlider::groove:horizontal {{
        height: 6px;
        background: {BDR};
        border-radius: 3px;
    }}
    QSlider::sub-page:horizontal {{
        background: {PRI};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        width: 20px; height: 20px;
        background: {PRI};
        border-radius: 10px;
        margin: -7px 0;
        border: 3px solid {CARD};
    }}
    QSlider::handle:horizontal:hover  {{ background: {PRI_H}; }}
    QSlider::handle:horizontal:pressed {{ background: {PRI_A}; }}

    /* ── ProgressBar ───────────────────── */
    QProgressBar {{
        background: {BDR};
        border-radius: 7px;
        border: none;
        min-height: 12px;
        max-height: 12px;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {PRI}, stop:1 #818CF8
        );
        border-radius: 7px;
    }}

    /* ── Named Labels ──────────────────── */
    QLabel#title {{
        font-size: 22px;
        font-weight: 700;
        color: {TXT};
    }}
    QLabel#subtitle {{
        font-size: 13px;
        color: {TXT2};
    }}
    QLabel#section_lbl {{
        font-size: 11px;
        font-weight: 700;
        color: {TXT3};
        letter-spacing: 1.2px;
    }}
    QLabel#count_badge {{
        background: {PRI};
        color: {PRI_T};
        border-radius: 10px;
        padding: 2px 9px;
        font-size: 11px;
        font-weight: 700;
    }}
    QLabel#stat_lbl {{
        font-size: 12px;
        color: {TXT2};
    }}
    QLabel#result_ok {{
        color: {OK};
        font-size: 13px;
        font-weight: 600;
    }}
    QLabel#result_err {{
        color: {ERR};
        font-size: 13px;
        font-weight: 600;
    }}
    """
