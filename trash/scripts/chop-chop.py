import os
import requests
from PIL import Image

BASE_URL_PNG = "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/{code}?wid=4608&hei=4608&fmt=png"
BASE_URL_JPG = "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/{code}?wid=1024&hei=1024&fmt=jpg&qlt=95"
x_pixels_to_crop = 100  # Number of pixels to crop from the left and right


def download_image(code, folder, img_type):
    file_path = os.path.join(folder, f"{code}.{img_type}")

    # If file already exists, skip the download
    if os.path.exists(file_path):
        print(f"File {code}.{img_type} already exists in {folder}. Skipping download.")
        return

    url = BASE_URL_PNG if img_type == "png" else BASE_URL_JPG
    url = url.format(code=code)

    response = requests.get(url, stream=True)

    if "Asset Not Found" in response.text:
        print(f"Image {code}.{img_type} not found!")
        return

    os.makedirs(folder, exist_ok=True)
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Downloaded {code}.{img_type} to {folder}")


def create_collage(folder_name):
    cropped_images = []
    cropped_filenames = []

    for filename in sorted(os.listdir(folder_name)):
        if (
            filename.endswith(".jpg")
            and not filename.endswith("_cropped.jpg")
            and not filename.startswith(folder_name)
        ):
            image_path = os.path.join(folder_name, filename)
            with Image.open(image_path) as img:
                width, height = img.size
                new_img = img.crop(
                    (x_pixels_to_crop, 0, width - x_pixels_to_crop, height)
                )
                cropped_images.append(new_img)

                # Save cropped image with '_cropped' suffix
                cropped_filename = filename.replace(".jpg", "_cropped.jpg")
                new_img.save(os.path.join(folder_name, cropped_filename))
                cropped_filenames.append(cropped_filename)

    # Combining images side by side
    total_width = sum(img.width for img in cropped_images)
    max_height = max(img.height for img in cropped_images)

    combined_img = Image.new("RGB", (total_width, max_height))
    x_offset = 0
    for img in cropped_images:
        combined_img.paste(img, (x_offset, 0))
        x_offset += img.width

    combined_img_filename = f"{folder_name}.jpg"
    combined_img.save(os.path.join(folder_name, combined_img_filename), quality=95)

    print(f"Combined collage saved to {folder_name}")

    # Clean up: Remove the cropped images
    for cropped_filename in cropped_filenames:
        os.remove(os.path.join(folder_name, cropped_filename))
    print(f"Cleaned up cropped images in {folder_name}")


def process_input_file(file_path):
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    folder_name = None
    models = []

    for line in lines:
        if line.endswith(":"):
            if folder_name:
                for model in models:
                    for img_type in ["png"]:  # , "jpg"
                        download_image(model, folder_name, img_type)
                create_collage(folder_name)
                models = []
            folder_name = line[:-1]
        else:
            models.append(line)

    if folder_name:
        for model in models:
            for img_type in ["png"]:  # , "jpg"
                download_image(model, folder_name, img_type)
        # create_collage(folder_name)


if __name__ == "__main__":
    # file_path = input("Please provide the path to the input file: ").strip()
    process_input_file("models.txt")
