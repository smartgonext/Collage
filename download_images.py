import os
import subprocess
import sys

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Ensure gdown is installed
install_and_import('gdown')

import gdown

def main():
    folder_url = 'https://drive.google.com/drive/folders/1a2JFS51reamumWu9JiMiZv71Y-hlCcgN'
    output_dir = os.path.join(os.getcwd(), 'images')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    print(f"Downloading images from Google Drive folder {folder_url} to {output_dir}...")
    try:
        # download_folder downloads all files inside the folder
        gdown.download_folder(url=folder_url, output=output_dir, quiet=False, use_cookies=False)
        print("Download completed successfully!")
    except Exception as e:
        print(f"Error downloading folder: {e}")

if __name__ == '__main__':
    main()
