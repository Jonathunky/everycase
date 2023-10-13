from PIL import Image
import os


def compress_and_resize_image(input_path, output_path, max_size=1536, quality=90):
    """
    Compress and resize an image to .webp format.

    Parameters:
    - input_path: Path to the source image.
    - output_path: Path to save the compressed image.
    - max_size: Maximum width and height for the output image.
    - quality: Quality for .webp compression (0 to 100).
    """

    # Open an image file
    with Image.open(input_path) as im:
        # Resize the image, preserving the aspect ratio
        im.thumbnail((max_size, max_size))
        # Save the image in .webp format with specified quality
        im.save(output_path, "WEBP", quality=quality)


if __name__ == "__main__":
    # Define the source and destination directories
    src_directory = "path_to_source_directory"
    dst_directory = "path_to_destination_directory"

    if not os.path.exists(dst_directory):
        os.makedirs(dst_directory)

    # Iterate over all files in the source directory
    for filename in os.listdir(src_directory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            src_path = os.path.join(src_directory, filename)
            dst_path = os.path.join(
                dst_directory, os.path.splitext(filename)[0] + ".webp"
            )
            compress_and_resize_image(src_path, dst_path)

    print("Image compression and resizing completed!")
