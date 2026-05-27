import os
import glob
import re
import subprocess
import sys

def main():
    print("=== STARTING MEMORA2K26 PIPELINE ===")
    
    # 1. Run the downloader
    print("\n--- Step 1: Downloading all images ---")
    downloader_script = os.path.join(os.getcwd(), 'download_all_images.py')
    if os.path.exists(downloader_script):
        try:
            subprocess.run([sys.executable, downloader_script], check=True)
            print("Download completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Downloader failed: {e}")
            print("Proceeding to optimization with whatever files downloaded successfully...")
    else:
        print("Error: download_all_images.py not found!")
        return

    # 2. Run the optimizer
    print("\n--- Step 2: Optimizing all downloaded images ---")
    optimizer_script = os.path.join(os.getcwd(), 'optimize_images.py')
    if os.path.exists(optimizer_script):
        try:
            subprocess.run([sys.executable, optimizer_script], check=True)
            print("Optimization completed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Optimizer failed: {e}")
            return
    else:
        print("Error: optimize_images.py not found!")
        return

    # 3. Scan optimized_images and update index.html
    print("\n--- Step 3: Updating index.html gallery array ---")
    dest_dir = os.path.join(os.getcwd(), 'optimized_images')
    jpg_files = glob.glob(os.path.join(dest_dir, "*.jpg"))
    # Sort them naturally/alphabetically
    relative_paths = sorted([f"optimized_images/{os.path.basename(f)}" for f in jpg_files])
    
    index_path = os.path.join(os.getcwd(), 'index.html')
    if not os.path.exists(index_path):
        print(f"Error: index.html not found at {index_path}")
        return
        
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Format the new array content nicely
    array_items = ",\n                ".join([f"'{path}'" for path in relative_paths])
    new_array = f"const galleryImages = [\n                {array_items}\n            ];"
    
    # Match const galleryImages = [ ... ];
    pattern = r'const galleryImages\s*=\s*\[[^\]]*\];'
    
    if re.search(pattern, content):
        updated_content = re.sub(pattern, new_array, content)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"SUCCESS: index.html updated with {len(relative_paths)} optimized images!")
    else:
        print("ERROR: Could not find galleryImages array in index.html")

    print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")

if __name__ == '__main__':
    main()
