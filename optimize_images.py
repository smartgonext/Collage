import os
import glob
import subprocess
import sys

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure required libraries are installed
install_package("rawpy")
install_package("PIL") # pillow is imported as PIL

from PIL import Image
import rawpy

def optimize_image(src_path, dest_path, max_size=(1200, 1200), quality=80):
    try:
        print(f"Processing image: {src_path}")
        img = None
        ext = os.path.splitext(src_path)[1].lower()
        
        if ext == '.arw':
            # Handle ARW (Sony Raw) file
            with rawpy.imread(src_path) as raw:
                try:
                    # Attempt to extract embedded thumbnail (super fast)
                    thumb = raw.extract_thumb()
                    if thumb.format == rawpy.ThumbFormat.JPEG:
                        import io
                        img = Image.open(io.BytesIO(thumb.data))
                        print("-> Successfully extracted embedded JPEG thumbnail.")
                    else:
                        print("-> Embedded thumbnail is not in JPEG format. Postprocessing RAW data...")
                        rgb = raw.postprocess(use_camera_wb=True, half_size=True) # half_size is faster and smaller
                        img = Image.fromarray(rgb)
                except Exception as thumb_err:
                    print(f"-> Thumbnail extraction failed ({thumb_err}). Postprocessing RAW data...")
                    rgb = raw.postprocess(use_camera_wb=True, half_size=True)
                    img = Image.fromarray(rgb)
        else:
            # Handle regular image formats (JPEG, PNG, etc.)
            img = Image.open(src_path)
            # Convert to RGB if in RGBA mode and saving as JPEG
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGB')
        
        if img:
            # Resize image maintaining aspect ratio
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save as optimized progressive JPEG
            img.save(dest_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            print(f"-> Saved optimized image to: {dest_path} ({os.path.getsize(dest_path) // 1024} KB)")
            return True
    except Exception as e:
        print(f"Error optimizing {src_path}: {e}")
        return False

def main():
    src_dir = os.path.join(os.getcwd(), 'images')
    dest_dir = os.path.join(os.getcwd(), 'optimized_images')
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory: {dest_dir}")
        
    # Supported formats
    extensions = ['*.arw', '*.ARW', '*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG']
    files_to_process = []
    for ext in extensions:
        files_to_process.extend(glob.glob(os.path.join(src_dir, ext)))
        
    # Remove duplicates
    files_to_process = list(set(files_to_process))
    print(f"Found {len(files_to_process)} files to process in {src_dir}")
    
    success_count = 0
    for file_path in files_to_process:
        # Ignore partial downloads
        if file_path.endswith('.part'):
            continue
            
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        dest_path = os.path.join(dest_dir, f"{base_name.lower()}.jpg")
        
        if optimize_image(file_path, dest_path):
            success_count += 1
            
    print(f"\nSuccessfully optimized {success_count} / {len(files_to_process)} images!")

if __name__ == '__main__':
    main()
