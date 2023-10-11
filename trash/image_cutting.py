from PIL import Image
import os

# Directory containing the images
image_directory = "./iphone-12/"
output_directory = "./modified/"
x_pixels_to_crop = 200  # Change this value to the number of pixels you want to crop

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

cropped_images = []

for filename in sorted(os.listdir(image_directory)):
    if filename.endswith((".jpg", ".jpeg")):
        image_path = os.path.join(image_directory, filename)
        with Image.open(image_path) as img:
            width, height = img.size
            new_img = img.crop((x_pixels_to_crop, 0, width - x_pixels_to_crop, height))
            cropped_images.append(new_img)
            new_img.save(os.path.join(output_directory, filename))

# Combining images side by side
total_width = sum(img.width for img in cropped_images)
max_height = max(img.height for img in cropped_images)

combined_img = Image.new("RGB", (total_width, max_height))

x_offset = 0
for img in cropped_images:
    combined_img.paste(img, (x_offset, 0))
    x_offset += img.width

combined_img.save(os.path.join(output_directory, "combined_image.jpg"), quality=95)
