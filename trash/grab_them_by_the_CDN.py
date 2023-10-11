import os
import requests

BASE_URL_PNG = "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/{code}?wid=4500&hei=4500&fmt=png"
BASE_URL_JPG = "https://store.storeimages.cdn-apple.com/8756/as-images.apple.com/is/{code}?wid=1000&hei=1000&fmt=jpg&qlt=95"


def download_image(code, folder, img_type):
    url = BASE_URL_PNG if img_type == "png" else BASE_URL_JPG
    url = url.format(code=code)

    response = requests.get(url, stream=True)

    if "Asset Not Found" in response.text:
        print(f"Image {code}.{img_type} not found!")
        return

    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, f"{code}.{img_type}"), "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"Downloaded {code}.{img_type} to {folder}")


def process_input_file(file_path):
    with open(file_path, "r") as f:
        lines = f.read().splitlines()

    folder_name = None
    models = []

    for line in lines:
        if line.endswith(":"):
            if folder_name:
                for model in models:
                    for img_type in ["png", "jpg"]:
                        download_image(model, folder_name, img_type)
                models = []
            folder_name = line[:-1]  # Removing the colon at the end
        else:
            models.append(line)

    # For the last set of models after the loop
    if folder_name:
        for model in models:
            for img_type in ["png", "jpg"]:
                download_image(model, folder_name, img_type)


if __name__ == "__main__":
    file_path = input("Please provide the path to the input file: ").strip()
    process_input_file(file_path)
