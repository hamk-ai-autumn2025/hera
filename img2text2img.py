# img2text2img.py
# -------------------------------------------
# 1) Lukee kuvan
# 2) Kuvailee sen (Vision)
# 3) Tulostaa kuvauksen stdoutiin
# 4) Generoi uuden kuvan kuvauksen perusteella
#
# ÄLÄ tallenna API-keytä koodiin. Ohjelma kysyy sen tarvittaessa.
# Vaihtoehtoisesti voit asettaa avaimen ennen ajoa:
#   $Env:OPENAI_API_KEY="sk-..."   (PowerShell)
# -------------------------------------------

import os, sys, base64, argparse, mimetypes

def _get_client():
    from openai import OpenAI
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        # Piilotettu syöttö; ei tulostu ruudulle
        try:
            import getpass
            key = getpass.getpass("OpenAI API key (sk-…): ").strip()
        except Exception:
            key = input("OpenAI API key (sk-…): ").strip()
        if not key.startswith("sk-"):
            print("ERROR: API key näyttää virheelliseltä (alkaa yleensä 'sk-').", file=sys.stderr)
            sys.exit(1)
        os.environ["OPENAI_API_KEY"] = key
    return OpenAI(api_key=key)

def _validate_size(size: str) -> str:
    allowed = {"1024x1024", "1024x1536", "1536x1024", "auto"}
    if size == "512x512":
        print("[INFO] 512x512 ei ole tuettu, käytetään 1024x1024.", file=sys.stderr)
        return "1024x1024"
    if size not in allowed:
        print(f"ERROR: Size '{size}' ei ole tuettu. Sallitut: {', '.join(sorted(allowed))}.", file=sys.stderr)
        sys.exit(1)
    return size

def b64_data_uri(path: str) -> str:
    if not os.path.isfile(path):
        print(f"ERROR: Tiedostoa ei löydy: {path}", file=sys.stderr); sys.exit(1)
    mime, _ = mimetypes.guess_type(path)
    if mime is None: mime = "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

def describe_image(client, data_uri: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a precise image describer."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe this image in 2–4 sentences, objectively and concretely."},
                    {"type": "image_url", "image_url": {"url": data_uri}}
                ]}
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] Vision-kuvaus epäonnistui: {e}", file=sys.stderr)
        sys.exit(2)

def generate_image(client, prompt: str, size: str, out_path: str):
    try:
        img = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size=size,
        )
        img_b64 = img.data[0].b64_json
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(img_b64))
    except Exception as e:
        print(f"[ERROR] Kuvagenerointi epäonnistui: {e}", file=sys.stderr)
        sys.exit(3)

def main():
    ap = argparse.ArgumentParser(description="Image -> text -> image")
    ap.add_argument("image", help="Polku syötekuvaan (jpg/png/webp)")
    ap.add_argument("--size", default="1024x1024",
                    help="Uuden kuvan koko: 1024x1024, 1024x1536, 1536x1024 tai auto")
    ap.add_argument("--out", default="out.png", help="Uuden kuvan tiedostonimi")
    args = ap.parse_args()

    size = _validate_size(args.size)
    client = _get_client()

    data_uri = b64_data_uri(args.image)
    description = describe_image(client, data_uri)

    # 3) Tulostus STDOUTiin (tehtävän vaatimus)
    print(description)

    # 4) Generointi
    generate_image(client, description, size, args.out)
    print(f"\n[OK] Generated image saved to: {args.out}", file=sys.stderr)

if __name__ == "__main__":
    main()
