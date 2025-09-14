import argparse
import requests
import os
import uuid
from dotenv import load_dotenv

# Lataa ympäristömuuttujat .env-tiedostosta
load_dotenv()
API_KEY = os.getenv("HUGGINGFACE_API_KEY")
GYAZO_ACCESS_TOKEN = os.getenv("GYAZO_ACCESS_TOKEN")

# Hugging Face API-asetukset
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Kuvasuhteen muunnos pikseleiksi
def parse_aspect_ratio(ratio_str):
    ratios = {
        "1:1": (512, 512),
        "16:9": (768, 432),
        "4:3": (640, 480),
        "3:4": (480, 640)
    }
    return ratios.get(ratio_str, (512, 512))

# Lataa kuva Gyazoon
def upload_to_gyazo(image_path):
    with open(image_path, 'rb') as img_file:
        response = requests.post(
            url="https://upload.gyazo.com/api/upload",
            headers={"Authorization": f"Bearer {GYAZO_ACCESS_TOKEN}"},
            files={"imagedata": img_file}
        )
    if response.status_code == 200:
        return response.json().get('url')
    else:
        print(f"Error uploading to Gyazo: {response.status_code} - {response.text}")
        return None

# Kuvien generointi ja lataus Gyazoon
def generate_images(prompt, negative_prompt, seed, aspect_ratio, num_images):
    width, height = aspect_ratio
    filenames = []

    for i in range(num_images):
        parameters = {
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height
        }
        if seed is not None:
            parameters["seed"] = seed

        payload = {
            "inputs": prompt,
            "parameters": parameters
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            image_data = response.content
            filename = f"image_{uuid.uuid4().hex}.png"
            with open(filename, "wb") as f:
                f.write(image_data)
            print(f"Image saved: {filename}")
            gyazo_url = upload_to_gyazo(filename)
            if gyazo_url:
                print(f"Image URL: {gyazo_url}")
            filenames.append(filename)
        else:
            print(f"Error generating image {i+1}: {response.status_code} - {response.text}")

    return filenames

# Komentoriviparametrien käsittely
def main():
    parser = argparse.ArgumentParser(description="Image Generator with Hugging Face and Gyazo")
    parser.add_argument("--prompt", required=True, help="Image description prompt")
    parser.add_argument("--negative_prompt", default="", help="Negative prompt to avoid certain features")
    parser.add_argument("--seed", type=int, default=None, help="Seed value for reproducibility")
    parser.add_argument("--aspect_ratio", default="1:1", choices=["1:1", "16:9", "4:3", "3:4"], help="Aspect ratio of the image")
    parser.add_argument("--num_images", type=int, default=1, help="Number of images to generate")

    args = parser.parse_args()
    aspect = parse_aspect_ratio(args.aspect_ratio)
    generate_images(args.prompt, args.negative_prompt, args.seed, aspect, args.num_images)

if __name__ == "__main__":
    main()
