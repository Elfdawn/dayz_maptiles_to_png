import os
from PIL import Image

# Define the size of the grid -> Chernarus+ is 32
grid_size = 32

# PNG Images contain a 16px overlap with each image.
trim_pixels = 16

image_directory = "your_directory_here"

images = {}

for filename in os.listdir(image_directory):
    if  filename.startswith("S") and filename.endswith(".png"): # S For topographical / M for Heat
        # Extract the X and Y coordinates from the filename
        base_name = filename.split('.')[0]  # S_000_000
        _, x_str, y_str, crap = filename.split('_')
        x = int(x_str)
        y = int(y_str)
        
        # Open the image
        image_path = os.path.join(image_directory, filename)
        img = Image.open(image_path)
        # Crop the image to remove the extra pixels
        width, height = img.size
        cropped_img = img.crop((trim_pixels, trim_pixels, width - trim_pixels, height - trim_pixels))
        # Store the image in the dictionary with its coordinates
        images[(x, y)] = cropped_img
        print(f" {filename} stored")

# Assume all images have the same dimensions
sample_image = next(iter(images.values()))
image_width, image_height = sample_image.size

# Create a blank canvas to hold the final stitched image
stitched_image = Image.new('RGB', (image_width * grid_size, image_height * grid_size))

# Paste each image into the correct position on the canvas
for (x, y), img in images.items():
    x_offset = x * image_width
    y_offset = y * image_height
    stitched_image.paste(img, (x_offset, y_offset))

# Save the final stitched image
stitched_image.save("dayz_full_map.png")

print("Image saved as dayz_full_map.png!")

