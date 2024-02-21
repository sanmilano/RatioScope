import gradio as gr
from PIL import Image
from collections import Counter
import numpy as np
import os

#First Tab: Sort Images by Aspect Ratios

# Define your desired aspect ratios
aspect_ratios = [16/9, 9/16, 4/5, 5/4, 1, 4/3, 3/4, 2/3, 3/2]
aspect_ratio_strings = ["16:9", "9:16", "4:5", "5:4", "1:1", "4:3", "3:4", "2:3", "3:2"]
aspect_ratio_dict = dict(zip(aspect_ratios, aspect_ratio_strings))

def closest_aspect_ratio(width, height, aspect_ratios):
    image_ratio = width / height
    return min(aspect_ratios, key=lambda x:abs(x - image_ratio))

def sort_images(image_folder, output_folder, aspect_ratios):
    if not os.path.exists(image_folder):
        return f"The specified folder does not exist. Please check the path and try again."
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

def sort_images_by_aspect_ratio(image_folder, output_folder, aspect_ratios):
    if len(aspect_ratios) < 2 or len(aspect_ratios) > 4:
        return "Select at least 2 aspect ratios and up to 4."
    aspect_ratios = [eval(ratio.replace(':', '/')) for ratio in aspect_ratios]
    result = sort_images(image_folder, output_folder, aspect_ratios)
    if result:
        return result
    return f"Images sorted and saved in {output_folder}"

#Second Tab: Resize and Crop Images to a Desired Resolution

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    new_width, new_height = map(int, size.split(' x '))

    # Calculate the aspect ratio of the image and the target size
    image_aspect_ratio = original_image.width / original_image.height
    target_aspect_ratio = new_width / new_height

    # Resize the image to fit within the target size, maintaining aspect ratio
    if image_aspect_ratio > target_aspect_ratio:
        # If image is wider than the target size, constrain by height
        resized_image = original_image.resize((int(new_height * image_aspect_ratio), new_height))
    else:
        # If image is taller than the target size, constrain by width
        resized_image = original_image.resize((new_width, int(new_width / image_aspect_ratio)))

    # Calculate the area to be cropped
    left = (resized_image.width - new_width) / 2
    top = (resized_image.height - new_height) / 2
    right = (resized_image.width + new_width) / 2
    bottom = (resized_image.height + new_height) / 2

    # Crop the image to the target size
    cropped_image = resized_image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(output_image_path, "PNG")

def resize_images_in_folder(input_folder, output_folder, size):
    if not os.path.exists(input_folder):
        return f"The specified folder does not exist. Please check the path and try again."
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total_images = len([name for name in os.listdir(input_folder) if name.endswith(".jpg") or name.endswith(".png") or name.endswith(".jpeg") or name.endswith(".webp") or name.endswith(".gif")])
    processed_images = 0

    for i, filename in enumerate(os.listdir(input_folder)):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".webp") or filename.endswith(".gif"):
            input_image_path = os.path.join(input_folder, filename)
            filename_without_ext = os.path.splitext(filename)[0]
            output_image_path = os.path.join(output_folder, filename_without_ext + ".png")
            resize_image(input_image_path, output_image_path, size)
            processed_images += 1
            print(f"Processed {processed_images} of {total_images} images.")

    return f"Processed {processed_images} of {total_images}. Images resized and saved in {output_folder}"

def resize_images(input_folder, output_folder, size, custom_width, custom_height):
    if not input_folder:
        return "Please provide an input folder."
    if not output_folder:
        return "Please provide an output folder."
    if not size and (not custom_width or not custom_height):
        return "Please select a resolution or enter a custom width and height."

    if custom_width and custom_height:
        size = f"{custom_width} x {custom_height}"

    return resize_images_in_folder(input_folder, output_folder, size)

def calculate_aspect_ratio(image):
    img = Image.fromarray(image.astype('uint8'))
    width, height = img.size
    closest_ratio = closest_aspect_ratio(width, height, aspect_ratios)
    return f"The closest aspect ratio for the uploaded image is {aspect_ratio_dict[closest_ratio]}."

resolutions = ["1344 x 768", "768 x 1344", "1024 x 1024", "896 x 1088", "1088 x 896", "1152 x 896", "896 x 1152", "1216 x 832", "832 x 1216", "Custom"]
aspect_ratio_options = ["16:9", "9:16", "4:5", "5:4", "1:1", "4:3", "3:4", "2:3", "3:2"]

#Third Tab: Caclulate Aspect Ratios

def calculate_aspect_ratios(folder_path):
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        return "The specified folder does not exist. Please check the path and try again."
    aspect_ratios = ["16:9", "1:1", "4:3", "3:2", "2:3", "3:4", "4:5", "5:4", "9:16"]
    aspect_ratio_counts = Counter()

    # Scan the folder and calculate aspect ratio for each image
    for filename in os.listdir(folder_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            with Image.open(os.path.join(folder_path, filename)) as img:
                width, height = img.size
                # Calculate aspect ratio and find the closest predefined aspect ratio
                aspect_ratio = width / height
                closest_ratio = min(aspect_ratios, key=lambda x: abs(aspect_ratio - np.divide(*map(int, x.split(':')))))
                aspect_ratio_counts[closest_ratio] += 1
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    if not image_files:
        return "No images were found in that folder."

    # Calculate percentages and get the top 5
    total_images = sum(aspect_ratio_counts.values())
    top_5_ratios = aspect_ratio_counts.most_common(5)
    top_5_percentages = [(ratio, round(count / total_images * 100, 1)) for ratio, count in top_5_ratios]

    # Format the output as a string
    output = "; ".join(f"{ratio}, {percentage}%" for ratio, percentage in top_5_percentages)

    return output

with gr.Blocks(title="RatioScope", css="h1 {color: #0f766e}", theme=gr.themes.Base(primary_hue="teal", secondary_hue="yellow", neutral_hue="stone", font=[gr.themes.GoogleFont("Raleway"), "Arial", "sans-serif"])) as demo:
    gr.Markdown(
            """
            <h1>RatioScope</h1>
            <p>A tool designed for creating and organizing image datasets.</p>

            """, sanitize_html=False)
    with gr.Tab("Sort Images"):
        gr.Markdown(
            """
            <h2>Sort Images by Aspect Ratio</h2>
            <p>This app helps you declutter and organize your image datasets with ease. Simply select a folder containing your images, choose your desired aspect ratio (e.g., 16:9, 4:3, etc.), and let the app do its magic.<br />The app will scan each image, analyze its proportions, and sort them into separate folders based on their closest match to the chosen aspect ratio. This creates a tidy and efficient system for finding images with similar shapes and sizes.</p>

            """, sanitize_html=False)
        gr.Interface(fn=sort_images_by_aspect_ratio, 
                     inputs=[gr.Textbox(label="Image folder", placeholder="Write an input folder"), 
                             gr.Textbox(label="Output folder", placeholder="Write an output folder"), 
                             gr.CheckboxGroup(label="Aspect ratios", 
                                              choices=aspect_ratio_options)], 
                     outputs="text")
    with gr.Tab("Resize Images"):
        gr.Markdown(
            """
            <h2>Resize Images to a Desired Resolution</h2>
            <p>This app simplifies batch image resizing and cropping. Seelect a folder, specify the desired resolution, and the tool resizes images without compromising quality. It analyzes and crops each image precisely, eliminating excess pixels without distortion. The result is an organized collection of images, all resized and cropped to the specified resolution.</p>

            """, sanitize_html=False)
        gr.Interface(fn=resize_images, 
                     inputs=[gr.Textbox(label="Input folder", placeholder="Write an input folder"), 
                             gr.Textbox(label="Output folder", placeholder="Write an output folder"), 
                             gr.Dropdown(choices=resolutions, label="Size"), 
                             gr.Textbox(label="Custom Width", placeholder="Write an custom Width"), 
                             gr.Textbox(label="Custom Height", placeholder="Write an custon Height")], 
                     outputs="text")
    with gr.Tab("Calculate Aspect Ratio"):
        gr.Markdown(
            """
            <h2>Calculate the Aspect Ratio</h2>
            <p>This app simplifies aspect ratio calculations for your image dataset. By selecting a single image or an entire folder, it swiftly computes the aspect ratios and presents the top 5 results. This functionality empowers users to effortlessly organize their images based on proportional dimensions, ensuring a streamlined and efficient approach to managing their dataset.</p>

            """, sanitize_html=False)
        with gr.Accordion("Single Image"):
            gr.Interface(fn=calculate_aspect_ratio, 
                         inputs=[gr.Image(label="Upload Image", sources="upload")], 
                         outputs="text")
        with gr.Accordion("Batch Images"):
            gr.Interface(fn=calculate_aspect_ratios, 
                         inputs=[gr.Textbox(label="Input folder", placeholder="Write an input folder")], 
                         outputs="text")
    with gr.Tab("Resolutions Cheatsheet"):
                gr.Markdown(
                    """
                    <h2>Resolutions and Aspect Ratios Cheatsheet</h2>
                    <p>This resource serves as a guide to the most prevalent aspect ratios, along with their corresponding resolutions based on the training of the base model.</p>

                    """, sanitize_html=False)
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown(
                            """
                            <h3>Stable Diffusion XL (SDXL)</h3>
                            <table>
                                <tr>
                                    <th>Resolution</th>
                                    <th>Aspect Ratio</th>
                                </tr>
                                <tr>
                                    <td>1344 x 768</td>
                                    <td>Approximately 16:9</td>
                                </tr>
                                <tr>
                                    <td>768 x 1344</td>
                                    <td>Approximately 9:16</td>
                                </tr>
                                <tr>
                                    <td>1024 x 1024</td>
                                    <td>1:1</td>
                                </tr>
                                <tr>
                                    <td>1088 x 896</td>
                                    <td>5:4, an aspect ratio popular in photography</td>
                                </tr>
                                <tr>
                                    <td>896 x 1088</td>
                                    <td>4:5, an aspect ratio popular in photography</td>
                                </tr>
                                <tr>
                                    <td>1152 x 896</td>
                                    <td>4:3</td>
                                </tr>
                                <tr>
                                    <td>896 x 1153</td>
                                    <td>3:4</td>
                                </tr>
                                <tr>
                                    <td>1216 x 832</td>
                                    <td>Closest to 3:2, the classic 35mm photography aspect ratio</td>
                                </tr>
                                <tr>
                                    <td>832 x 1216</td>
                                    <td>Closest to 2:3, the classic 35mm photography aspect ratio</td>
                                </tr>
                                </table>
                            """, sanitize_html=False)
                    with gr.Column(scale=1):
                        gr.Markdown(
                            """
                            <h3>Stable Diffusion 1.5</h3>
                            <p>Available on next update.</p>
                            """, sanitize_html=False)
    gr.Markdown(
            """
            <small>Created by <a href='https://github.com/sanmilano'>San Milano</a>.</small>

            """, sanitize_html=False)
            

demo.launch()