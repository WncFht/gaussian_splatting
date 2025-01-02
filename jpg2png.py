import os
from PIL import Image

def convert_jpg_to_png(directory):
    """
    Convert all .jpg images in the given directory to .png.

    Args:
        directory (str): Path to the directory containing .jpg images.

    Returns:
        None
    """
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return

    for filename in os.listdir(directory):
        # Check if the file has a .jpg extension
        if filename.lower().endswith(".jpg"):
            jpg_path = os.path.join(directory, filename)
            png_path = os.path.join(directory, os.path.splitext(filename)[0] + ".png")

            try:
                # Open the .jpg image and save it as .png
                with Image.open(jpg_path) as img:
                    img.save(png_path, "PNG")
                print(f"Converted: {jpg_path} -> {png_path}")

                # Optionally, remove the original .jpg file
                os.remove(jpg_path)
                print(f"Deleted: {jpg_path}")

            except Exception as e:
                print(f"Error converting {jpg_path}: {e}")

def main():
    directory = input("Please provide the path to the directory containing .jpg images: ").strip()
    convert_jpg_to_png(directory)

if __name__ == "__main__":
    main()
