import os
import re
import pathlib
import pandas as pd
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv

def sanitize_filename(name):
    """Sanitizes a string to be a valid filename."""
    name = name.lower()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^a-z0-9_.]', '', name)
    return name

def main():
    """Main function to generate images from prompts in a CSV file."""
    # Load environment variables from .env file
    load_dotenv()

    # --- 1. Context & Setup ---
    try:
        api_key = os.environ['GEMINI_API_KEY']
        genai.configure(api_key=api_key)
    except KeyError:
        print("Error: GEMINI_API_KEY environment variable not found.")
        print("Please create a .env file and add your API key: GEMINI_API_KEY='your_key_here'")
        return

    # --- 2. Validation Step ---
    current_dir = pathlib.Path('.')
    image_files = (list(current_dir.glob('*.png')) +
                   list(current_dir.glob('*.jpg')) +
                   list(current_dir.glob('*.jpeg')))
    csv_files = list(current_dir.glob('*.csv'))

    if len(image_files) != 1:
        print(f"Error: Expected 1 image file (png, jpg, jpeg), but found {len(image_files)}.")
        return
    original_image_path = image_files[0]

    if len(csv_files) != 1:
        print(f"Error: Expected 1 CSV file, but found {len(csv_files)}.")
        return
    prompts_csv_path = csv_files[0]

    print(f"Using image: {original_image_path}")
    print(f"Using CSV: {prompts_csv_path}")

    # --- 3. Reading the CSV ---
    try:
        df = pd.read_csv(prompts_csv_path)
        if "Prompt (English)" not in df.columns or "Scene Name" not in df.columns:
            print("Error: CSV must contain 'Prompt (English)' and 'Scene Name' columns.")
            return
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file at {prompts_csv_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV: {e}")
        return

    # --- 4. The Generation Loop ---
    output_dir = pathlib.Path('output_images')
    output_dir.mkdir(exist_ok=True)

    # Using the user-specified model: 'gemini-3-pro-image-preview'.
    model = genai.GenerativeModel('gemini-3-pro-image-preview')

    # Prepare the image data once
    image_bytes = original_image_path.read_bytes()
    image_mime_type = 'image/png' if original_image_path.suffix.lower() == '.png' else 'image/jpeg'
    original_image_part = {
        'mime_type': image_mime_type,
        'data': image_bytes
    }

    for index, row in df.iterrows():
        scene_name = row["Scene Name"]
        prompt_text = row["Prompt (English)"]
        sanitized_name = sanitize_filename(scene_name) + ".png"
        output_path = output_dir / sanitized_name

        print(f"\nProcessing row {index + 1}: '{scene_name}'")

        try:
            # --- 4a. Generate Image ---
            # Constructing the request with an explicit image part dictionary
            response = model.generate_content(
                [
                    "Generate a new image based on this original character. The new image should place the character in the following scene or context described in the text. The final image should be a 1:1 square aspect ratio.",
                    original_image_part,
                    prompt_text,
                ],
            )
            
            # --- 5. Saving the Outputs ---
            # The new library structure returns the image data in response.parts
            if response.parts:
                # Assuming the first part is the generated image
                generated_image_blob = response.parts[0].inline_data
                img_bytes = generated_image_blob.data
                
                with open(output_path, 'wb') as f:
                    f.write(img_bytes)
                print(f"  - Successfully saved to {output_path}")
            else:
                 print(f"  - Error: Generation failed for '{scene_name}'. The API did not return an image.")
                 # To debug, you can inspect the full response:
                 # print("Full API Response:", response)

        except Exception as e:
            print(f"  - Error: An API error occurred for '{scene_name}': {e}")
            continue # Gracefully continue to the next row


if __name__ == "__main__":
    main()
