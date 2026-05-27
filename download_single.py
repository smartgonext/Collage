import os
import gdown

def main():
    file_id = "1CqkEAhmgiA2QE4D0VAQMuXFJ0tSOM9f5"
    output_dir = os.path.join(os.getcwd(), "images")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Testing download for ID {file_id}...")
    try:
        # Let's specify output as output_dir + / which forces folder mode, or let gdown handle it.
        # Alternatively, we download to a temporary location or use gdown.download(id=file_id, quiet=False)
        # Note: gdown.download(id=file_id, output=None, quiet=False) will auto-name in the current directory,
        # then we can move it. Let's let gdown write directly.
        # To download into output_dir with auto-naming, we can pass output=os.path.join(output_dir, '')
        output_path = gdown.download(id=file_id, output=os.path.join(output_dir, ''), quiet=False)
        print(f"Downloaded to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
