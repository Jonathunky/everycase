import os
from PIL import Image


def resize_image(input_path, output_path):
    img = Image.open(input_path)
    img = img.resize((512, 512), Image.LANCZOS)
    img.save(output_path, "PNG")


def batch_resize(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            input_path = os.path.join(directory, filename)

            # Updated output path
            output_path = os.path.join("public", "everyphone", filename)

            resize_image(input_path, output_path)

            # Deleting the original image
            os.remove(input_path)


if __name__ == "__main__":
    batch_resize("trash/images")
