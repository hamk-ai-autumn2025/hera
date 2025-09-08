import os
from dotenv import load_dotenv
from embedchain import App
import argparse

# Lataa ympäristömuuttujat (esim. OpenAI API -avain .env-tiedostosta)
load_dotenv()

def main():
    parser = argparse.ArgumentParser(
        description="Anna tiedoston nimi tai URL ja kysy siitä kysymys."
    )
    parser.add_argument("sources", nargs="+", help="Tiedoston nimi tai URL (tai useampi)")
    parser.add_argument("-q", "--query", help="Kysymys sisällöstä")
    parser.add_argument("-f", "--file", help="Tallennetaan vastaus tiedostoon")
    args = parser.parse_args()

    # Luo Embedchain-sovellus
    app = App()

    # Lisää lähteet (tiedostot tai URLit)
    for src in args.sources:
        print(f"📥 Lisätään tietopankkiin: {src}")
        app.add(src)

    # Käyttäjän kysymys tai tiivistelmä
    question = args.query if args.query else "Tee tiivistelmä annetusta sisällöstä."
    print(f"💬 Kysymys: {question}")
    response = app.query(question)

    # Tulosta tai tallenna
    if args.file:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(response)
        print(f"✅ Vastaus tallennettu tiedostoon: {args.file}")
    else:
        print("🧠 Vastaus:")
        print(response)

if __name__ == "__main__":
    main()

