# 🛠️ Image Converter

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

A powerful, universal, and interactive Python script via Command Line Interface (CLI) to convert images from one format to another seamlessly. Originally built for HEIC to JPEG conversion, it has now evolved into a comprehensive image conversion tool.

Useful for converting photos, handling transparency (Alpha channel) automatically, and processing large batches of images effortlessly.

---

## ✨ Features

* **Multi-Format Support**: Convert to/from a wide variety of image formats.
* **Batch Conversion**: Convert entire folders of images at once.
* **Auto-Transparency Handling**: Automatically converts transparent backgrounds (like from PNGs) to solid white when converting to formats that don't support transparency (like JPEG or BMP), preventing black artifacts.
* **"Convert All" Feature**: Process a folder containing multiple different image formats and standardize them into a single target format.
* **Smart Skipping**: Automatically skips files that are already in the target output format.
* **Interactive CLI**: Easy-to-use command-line interface with detailed progress and summary output.
* Works natively on **macOS, Linux, and Windows**.

---

## 📦 Supported Output Formats

You can convert your images into any of these formats:
* `JPEG` / `JPG`
* `PNG`
* `WEBP`
* `BMP`
* `GIF`
* `TIFF`
* `ICO`
* `PDF`

*(Input formats can be any of the above, plus HEIC)*

---

## 🚀 Requirements

* Python **3.8+**
* `pip`

Python libraries required:
* `pillow`
* `pillow-heif`

---

## 🛠 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/codingnusantara/image-converter.git
   cd image-converter
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the environment:**
   * **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```
   * **Windows:**
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install pillow pillow-heif
   ```

---

## 📖 Usage

The script is executed via the terminal using `python convert.py` along with optional arguments. 

If you run `python convert.py` without arguments, it defaults to converting **HEIC files** in the **`photos` folder** to **JPG**.

Put your input images in the `photos` folder (or specify another folder using `-i`).

### Command Line Arguments

* `-i` or `--input_folder`: Folder containing images to convert (default: `photos`)
* `-f` or `--from_format`: Input format to convert from (e.g., `heic`, `png`, `webp`) or `all` to convert everything (default: `heic`)
* `-t` or `--to_format`: Output format to convert to (e.g., `jpg`, `png`, `webp`, `pdf`) (default: `jpg`)

---

### Examples

**1. Default Conversion (HEIC to JPG in `photos`):**
```bash
python convert.py
```

**2. Convert HEIC to PNG:**
```bash
python convert.py -f heic -t png
```

**3. Convert WEBP to JPG:**
```bash
python convert.py -f webp -t jpg
```

**4. Convert ALL images in the `photos` folder to WEBP:**
```bash
python convert.py -f all -t webp
```

**5. Convert HEIC to PDF in a specific folder named `holiday_pics`:**
```bash
python convert.py -i holiday_pics -f heic -t pdf
```

**6. Show help and list all parameters:**
```bash
python convert.py --help
```

---

## 📂 Project Structure

```
image-converter/
│
├── convert.py
├── photos/        <-- (Place your input files here)
│   ├── image1.heic
│   ├── image2.png
│   └── ...
└── README.md
```

---

## 📝 License

MIT License

Free to use, modify, and distribute.
