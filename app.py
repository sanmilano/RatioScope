import os
import shutil
from PIL import Image
import gradio as gr

# Define your desired aspect ratios
aspect_ratios = [1, 4/3, 16/9, 9/16]

def closest_aspect_ratio(width, height, aspect_ratios):
    image_ratio = width / height
    return min(aspect_ratios, key=lambda x:abs(x - image_ratio))

def sort_images(image_folder, output_folder, aspect_ratios):
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    total_images = len(images)
    for i, filename in enumerate(images):
        image_path = os.path.join(image_folder, filename)
        with Image.open(image_path) as img:
            width, height = img.size
            closest_ratio = closest_aspect_ratio(width, height, aspect_ratios)
            destination_folder = os.path.join(output_folder, str(closest_ratio))
            os.makedirs(destination_folder, exist_ok=True)
            png_filename = os.path.splitext(filename)[0] + '.png'
            destination_path = os.path.join(destination_folder, png_filename)
            img.save(destination_path, 'PNG')
        print(f"Processed {i+1} of {total_images} images.")

# Define the Gradio interface
def gradio_interface(image_folder, output_folder, aspect_ratios):
    if len(aspect_ratios) < 2 or len(aspect_ratios) > 4:
        return "Select at least 2 aspect ratios and up to 4."
    aspect_ratios = [eval(ratio.replace(':', '/')) for ratio in aspect_ratios]
    sort_images(image_folder, output_folder, aspect_ratios)
    return f"Images sorted and saved in {output_folder}"

aspect_ratio_options = ["16:9", "9:16", "4:5", "5:4", "1:1", "4:3", "3:4", "2:3", "3:2"]

iface = gr.Interface(fn=gradio_interface, 
                     inputs=[gr.components.Textbox(lines=1, label="Image folder:"), gr.components.Textbox(lines=1, label="Output folder:"), gr.components.CheckboxGroup(aspect_ratio_options, label="Aspect ratios:")], 
                     outputs="text",
                     title="RatioScope",
                     description="## Organize images by aspect ratio\n\nThis app helps you declutter and organize your image datasets with ease. Simply select a folder containing your images, choose your desired aspect ratio (e.g., 16:9, 4:3, etc.), and let the app do its magic.\n\nThe app will scan each image, analyze its proportions, and sort them into separate folders based on their closest match to the chosen aspect ratio. This creates a tidy and efficient system for finding images with similar shapes and sizes.",
                     article="Created by <a href='https://github.com/sanmilano'>San Milano</a>.")

iface.launch()