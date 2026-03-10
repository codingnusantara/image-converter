from typing import List, Tuple

APP_NAME    = "Image Converter"
APP_VERSION = "1.0"
MIN_W, MIN_H = 840, 640
DEF_W, DEF_H = 1000, 720

SUPPORTED_INPUTS = {
    "heic", "heif", "jpg", "jpeg", "png",
    "webp", "bmp", "gif", "tiff", "tif", "ico",
}

OUTPUT_FORMATS: List[Tuple[str, str, str]] = [
    ("JPEG",  "jpg",  "Best for photos · smaller files"),
    ("PNG",   "png",  "Lossless · preserves transparency"),
    ("WEBP",  "webp", "Modern format · tiny file size"),
    ("BMP",   "bmp",  "Uncompressed bitmap"),
    ("GIF",   "gif",  "Animation support"),
    ("TIFF",  "tiff", "Print quality"),
    ("ICO",   "ico",  "Windows icon format"),
    ("PDF",   "pdf",  "Portable Document Format"),
]

PIL_FORMAT_MAP = {
    "jpg": "JPEG", "jpeg": "JPEG", "png": "PNG",
    "webp": "WEBP", "bmp": "BMP", "gif": "GIF",
    "tiff": "TIFF", "ico": "ICO", "pdf": "PDF",
}

QUALITY_FMTS = {"jpg", "webp"}

# ─── Colour Palette ───────────────────────────────────────────────────────────
BG      = "#EBEEFF"   # window background
CARD    = "#FFFFFF"   # card / panel
CARD2   = "#F4F6FF"   # secondary card
BDR     = "#DDE1FF"   # border
BDR2    = "#AAAFFF"   # stronger border
PRI     = "#5C6BC0"   # indigo primary
PRI_H   = "#3F51B5"   # primary hover
PRI_A   = "#303F9F"   # primary active
PRI_L   = "#E8EAF6"   # primary light
PRI_T   = "#FFFFFF"   # text on primary buttons
TXT     = "#1B1E3C"   # dark text
TXT2    = "#5A5D80"   # medium text
TXT3    = "#9296B4"   # muted text
OK      = "#2E7D32"   # success
OK_BG   = "#E8F5E9"
ERR     = "#C62828"   # error
ERR_BG  = "#FFECEC"
WARN    = "#E65100"
ITEM_H  = "#EEEEFF"   # file item hover
