#!/usr/bin/env python3

import sys, io
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from PIL import Image

def generate_images_from_code(file_path, columns):
    with open(file_path, 'r') as f:
        code = f.read()

    # Syntax highlight the code and get it as an image
    highlighted_code = highlight(code, PythonLexer(), ImageFormatter(line_numbers=False))

    # Convert highlighted code to an Image object
    img = Image.open(io.BytesIO(highlighted_code))
    
    # Determine the width of the image corresponding to the desired number of columns
    char_width = img.width // len(code.split('\n')[0])
    desired_width = char_width * columns

    # Crop and save the images
    idx = 0
    top = 0
    bottom = img.height * desired_width // img.width
    while top < img.height:
        cropped_img = img.crop((0, top, desired_width, bottom))
        
        # Resize cropped image to 1920x1080
        resized_img = cropped_img.resize((1920, 1080))
        
        # Save the image
        output_path = f"./screenshots/{file_path.split('/')[-1]}_{idx}.png"
        resized_img.save(output_path)
        print(f"Saved: {output_path}")
        
        idx += 1
        top = bottom
        bottom = bottom + (img.height * desired_width // img.width)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: script_name.py <file_path> <number_of_columns>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    columns = int(sys.argv[2])
    
    generate_images_from_code(file_path, columns)
