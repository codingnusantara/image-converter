import argparse
import os
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener for HEIC support
register_heif_opener()

SUPPORTED_FORMATS = {
    'jpg': 'JPEG',
    'jpeg': 'JPEG',
    'png': 'PNG',
    'webp': 'WEBP',
    'bmp': 'BMP',
    'gif': 'GIF',
    'tiff': 'TIFF',
    'ico': 'ICO',
    'pdf': 'PDF'
}

def convert_image(input_path, output_path, output_format):
    try:
        with Image.open(input_path) as img:
            # Handle RGBA/LA -> RGB conversion for formats that don't support alpha channel
            if output_format in ['JPEG', 'BMP'] and img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background
                bg = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                bg.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                img = bg
            elif img.mode == 'P' and output_format not in ['GIF', 'PNG']:
                img = img.convert('RGB')

            # Save the image
            if output_format == 'JPEG':
                img.save(output_path, format=output_format, quality=95)
            elif output_format == 'WEBP':
                img.save(output_path, format=output_format, quality=95)
            else:
                img.save(output_path, format=output_format)
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="🛠️ Super Lengkap Image Converter")
    parser.add_argument("-i", "--input_folder", default="photos", help="Folder containing images to convert (default: 'photos')")
    parser.add_argument("-f", "--from_format", default="heic", help="Input format to convert from (e.g., heic, png, jpg, webp) or 'all' to convert everything")
    parser.add_argument("-t", "--to_format", default="jpg", help="Output format to convert to (e.g., jpg, png, webp, bmp, tiff, gif, pdf,ico)")
    
    args = parser.parse_args()

    input_folder = args.input_folder
    from_format = args.from_format.lower()
    to_format = args.to_format.lower()

    print("="*50)
    print(" 🛠️  SUPER LENGKAP IMAGE CONVERTER")
    print("="*50)

    if to_format not in SUPPORTED_FORMATS:
        print(f"❌ Error: Output format '{to_format}' is not supported.")
        print(f"✅ Supported output formats: {', '.join(SUPPORTED_FORMATS.keys())}")
        return

    pil_output_format = SUPPORTED_FORMATS[to_format]

    if not os.path.exists(input_folder):
        print(f"❌ Directory '{input_folder}' not found.")
        return

    print(f"📂 Folder Input  : {input_folder}")
    print(f"🔄 Format Asal   : {from_format.upper()}")
    print(f"🎯 Format Tujuan : {to_format.upper()}")
    print("-" * 50)

    converted_count = 0
    skipped_count = 0
    
    files = os.listdir(input_folder)
    
    if not files:
        print("📂 Folder kosong.")
        return

    for file in files:
        if from_format == "all" or file.lower().endswith(f".{from_format}"):
            input_path = os.path.join(input_folder, file)
            
            # Skip directories
            if os.path.isdir(input_path):
                continue
                
            filename, ext = os.path.splitext(file)
            
            # Skip if extension is already the target format
            if ext.lower().replace('.', '') == to_format:
                skipped_count += 1
                continue

            new_filename = f"{filename}.{to_format}"
            output_path = os.path.join(input_folder, new_filename)

            print(f"⏳ File: {file} -> {new_filename}...", end=" ")
            if convert_image(input_path, output_path, pil_output_format):
                print("✅ Sukses!")
                converted_count += 1
            else:
                print("❌ Gagal!")

    print("-" * 50)
    print(f"🎉 Selesai! Berhasil convert: {converted_count} file. Di-skip: {skipped_count} file.")
    print("="*50)

if __name__ == "__main__":
    main()
