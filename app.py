import streamlit as st
import os
import requests
import time

# Haetaan Replicate API -avain .env-tiedostosta (tai ympäristömuuttujista)
def read_env_token(filename=".env"):
    try:
        with open(filename, "r") as f:
            for line in f:
                if line.startswith("REPLICATE_API_TOKEN="):
                    return line.strip().split("=", 1)[1]
    except Exception as e:
        return None

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN") or read_env_token()

st.title("Stable Diffusion (Replicate) Kuvageneraattori")

prompt = st.text_input("Prompt (mitä kuvassa näkyy):", "")
negative_prompt = st.text_input("Negative prompt (mitä EI kuvassa):", "")
aspect_ratio = st.selectbox("Aspect ratio", ["1:1", "16:9", "4:3"])

def get_dimensions(ratio):
    if ratio == "1:1":
        return 512, 512
    if ratio == "16:9":
        return 704, 396
    if ratio == "4:3":
        return 512, 384
    return 512, 512

def generate_image(prompt, negative_prompt, aspect_ratio, REPLICATE_API_TOKEN):
    width, height = get_dimensions(aspect_ratio)
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "version": "ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",  # Tämä version id toimii varmasti
        "input": {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_inference_steps": 20,
            "scheduler": "K_EULER",  # Voit kokeilla muita, esim. "DPMSolverMultistep"
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 201:
        return None, response.text

    prediction = response.json()
    status = prediction["status"]
    prediction_url = prediction["urls"]["get"]

    while status not in ["succeeded", "failed"]:
        poll = requests.get(prediction_url, headers=headers)
        prediction = poll.json()
        status = prediction["status"]
        time.sleep(1)

    if status == "succeeded":
        return prediction["output"][0], None
    else:
        return None, str(prediction)

if st.button("Generate Image"):
    if not prompt:
        st.warning("Kirjoita prompt.")
    elif not REPLICATE_API_TOKEN or not REPLICATE_API_TOKEN.startswith("r8_"):
        st.error("API-avainta ei ladattu .env-tiedostosta. Tarkista että .env on oikeassa kansiossa ja rivin alku on REPLICATE_API_TOKEN=r8_...")
    else:
        with st.spinner("Kuvaa generoidaan..."):
            image_url, error = generate_image(prompt, negative_prompt, aspect_ratio, REPLICATE_API_TOKEN)
        if image_url:
            st.image(image_url, caption="Generoitu kuva")
            image_bytes = requests.get(image_url).content
            st.download_button("Download image", data=image_bytes, file_name="generated_image.png", mime="image/png")
        else:
            st.error("Kuvan generointi epäonnistui.")
            if error:
                st.code(error)