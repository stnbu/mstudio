import sys
import io
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from PIL import Image

def generate_images_from_code(file_path, columns):
    with open(file_path, 'r') as f:
        code = f.read()

    # Syntax highlight each line and save them as separate images
    lines = code.split('\n')
    line_images = []
    for line in lines:
        line_code = highlight(line, PythonLexer(), ImageFormatter(line_numbers=False))
        line_img = Image.open(io.BytesIO(line_code))
        line_images.append(line_img)

    # Calculate required height based on 56.25 lines
    target_height = int(56.25 * line_images[0].height)

    # Concatenate the images vertically
    idx = 0
    stacked_images = []
    while line_images:
        concatenated_img = Image.new('RGB', (line_images[0].width, 0))
        current_height = 0
        
        while current_height < target_height and line_images:
            current_img = line_images.pop(0)
            concatenated_img.paste(current_img, (0, current_height))
            current_height += current_img.height

        stacked_images.append(concatenated_img)

    # Crop and save the images
    if not os.path.exists('./screenshots'):
        os.makedirs('./screenshots')

    for idx, img in enumerate(stacked_images):
        # Crop the image to the desired width based on columns
        desired_width = columns * (img.width // min(len(line) for line in lines if line))
        cropped_img = img.crop((0, 0, desired_width, target_height))
        
        # Resize cropped image to 1920x1080
        resized_img = cropped_img.resize((1920, 1080))
        
        # Save the image
        output_path = f"./screenshots/{file_path.split('/')[-1]}_{idx}.png"
        resized_img.save(output_path)
        print(f"Saved: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: script_name.py <file_path> <number_of_columns>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    columns = int(sys.argv[2])
    
    generate_images_from_code(file_path, columns)
