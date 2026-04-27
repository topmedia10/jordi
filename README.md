# Gemini AI Image Generation Script

This project contains a Python script that automates the generation of images using the Google Gemini API. It uses a character reference image and a CSV file of prompts to generate a series of new images.

## Prerequisites

- Python 3.7+
- A Google Gemini API Key

## Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/topmedia10/jordi.git
    cd jordi
    ```

2.  **Create Environment File**
    - Create a file named `.env` in the root of the project directory.
    - Add your Gemini API key to this file:
      ```
      GEMINI_API_KEY='your_api_key_here'
      ```

3.  **Install Dependencies**
    - Install the required Python packages using pip:
      ```bash
      pip install -r requirements.txt
      ```

## How to Run

1.  **Place Your Files**
    - Place exactly ONE character reference image (e.g., `my_character.png`) in the root directory.
    - Place exactly ONE CSV file containing your prompts in the root directory. The CSV must have `"Scene Name"` and `"Prompt (English)"` columns.

2.  **Execute the Script**
    - Run the script from your terminal:
      ```bash
      python3 generate_images.py
      ```

## Output

The script will create a directory named `output_images` and save the generated images there. Each image will be named according to the "Scene Name" from the CSV file.
