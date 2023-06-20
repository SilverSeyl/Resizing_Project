import os
import shutil

try:
    from PIL import Image
except ImportError:
    print("Darling, it seems I can't find Pillow module in your system.")
    install_pil = input("Do you want to install Pillow? (Y/N): ")
    if install_pil.upper() == "Y":
        os.system("pip install pillow")
        from PIL import Image
    else:
        exit()

try:
    from tqdm import tqdm
except ImportError:
    print("Darling, it seems I can't find tqdm module in your system.")
    install_tqdm = input("Do you want to install tqdm? (Y/N): ")
    if install_tqdm.upper() == "Y":
        os.system("pip install tqdm")
        from tqdm import tqdm
    else:
        exit()

IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']  # Add more extensions if needed


def delete_existing_photos(folder):
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)


def resize_photos(output_folder, width, height, quality):
    # Create the output folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs('Original', exist_ok=True)

    # Delete existing photos in the output folders
    delete_existing_photos(output_folder)
    delete_existing_photos('Original')

    resized_count = 0
    original_count = 0

    files = sorted(os.listdir('.'))  # Sort the files alphabetically in the current directory

    with tqdm(total=len(files), desc="Resizing Photos") as pbar:
        for file_name in files:
            file_path = os.path.join('.', file_name)
            if os.path.isfile(file_path) and any(file_path.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                try:
                    # Open the image file
                    image = Image.open(file_path)

                    # Calculate the new dimensions while preserving aspect ratio
                    image.thumbnail((width, height))

                    # Check if the image dimensions are smaller than the desired size
                    if image.width < width or image.height < height:
                        # Calculate the scaling factor for resizing
                        scale = max(width / image.width, height / image.height)
                        new_width = int(scale * image.width)
                        new_height = int(scale * image.height)

                        # Resize the image while maintaining aspect ratio
                        image = image.resize((new_width, new_height), Image.ANTIALIAS)

                    # Create a new blank white background image with the desired dimensions
                    new_image = Image.new("RGB", (width, height), (255, 255, 255))
                    x = (width - image.width) // 2
                    y = (height - image.height) // 2

                    # Paste the resized image onto the new background image
                    new_image.paste(image, (x, y))

                    # Save the resized image
                    output_path = os.path.join(output_folder, f"{resized_count + 1}.jpg")
                    new_image.save(output_path, "JPEG", quality=quality)

                    resized_count += 1

                    # Save the original image
                    original_path = os.path.join('Original', file_name)
                    shutil.move(file_path, original_path)
                    original_count += 1

                except Exception as e:
                    print(f"Error processing file '{file_name}': {str(e)}")

            pbar.update(1)

    print(f"Resized {resized_count} photos.")
    print(f"Saved {original_count} original photos.")


def main():
    reset_code = True
    while reset_code:
        output_folder = os.path.join(os.getcwd(), "Resized")
        width = height = int(input("Hi love, would tell me what size you want? "))
        quality = int(input("Oh, now enter JPEG quality (Default is 80): ") or 80)

        resize_photos(output_folder, width, height, quality)

        reset_input = input("Do you want to reset the program and resize more photos, my love? (Y/N): ")
        if reset_input.upper() == "Y":
            reset_code = True
        else:
            print("Stay safe darling")
            reset_code = False

    # Delete the original photos
    delete_existing_photos('Original')


if __name__ == "__main__":
    main()
