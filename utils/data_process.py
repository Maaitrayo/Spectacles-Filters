import os
import glob

def rename_images(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Add more extensions if needed
    image_files = []

    for extension in image_extensions:
        image_files.extend(glob.glob(os.path.join(folder_path, '*' + extension)))

    for image_number, old_path in enumerate(image_files, start=1):
        _, extension = os.path.splitext(old_path)
        new_filename = f"specs_{image_number}{extension}"
        new_path = os.path.join(folder_path, new_filename)

        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")

if __name__ == "__main__":
    folder_path = "D:\DEVELOPMENT PROJECTS\WALLMART HACKATHON PROJECTS\E-Commerce-Product-Filters\DATASET\specs/"
    rename_images(folder_path)
