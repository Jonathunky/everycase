import os
from PIL import Image


def resize_image(input_path, output_path):
    img = Image.open(input_path)
    img = img.resize((1000, 1000))
    img.save(output_path, "PNG")


def batch_resize(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            input_path = os.path.join(directory, filename)
            output_path = os.path.join(
                directory, os.path.splitext(filename)[0] + "" + ".png"
            )
            resize_image(input_path, output_path)


if __name__ == "__main__":
    batch_resize("public/everyphone/")
