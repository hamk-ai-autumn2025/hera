import os
import argparse
from dotenv import load_dotenv
from embedchain import App

# Dokumenttityyppien tuki
SUPPORTED_EXTENSIONS = [".txt", ".csv", ".pdf", ".docx"]

# Ladataan API-avaimet ym.
load_dotenv()

def add_source(app, source):
    # URL
    if source.startswith("http://") or source.startswith("https://"):
        print(f"Lisätään nettisivu: {source}")
        app.add(source)
    # Tiedostot
    else:
        ext = os.path.splitext(source)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            print(f"Lisätään tiedosto: {source}")
            app.add(source)
        else:
            print(f"⚠️ Ei tuettu tiedostopääte: {source}")

def main():
    parser = argparse.ArgumentParser(
        description="Anna lähteitä (txt, csv, pdf, docx, url) ja kysy/vie tulos tiedostoon."
    )
    parser.add_argument("sources", nargs="+", help="Tiedostot ja/tai url:t")
    parser.add_argument("-q", "--query", help="Kysymys/summarointi")
    parser.add_argument("-f", "--file", help="Tallenna tulos tiedostoon")
    parser.add_argument("--reset", "-r", action="store_true", help="Nollaa Embedchainin tietopankki ennen uutta ajoa")
    args = parser.parse_args()

    app = App()
    if args.reset:
        print("🗑️ Nollataan Embedchainin tietopankki...")
        app.reset()

    for source in args.sources:
        add_source(app, source)

    question = args.query or "Tiivistä annetut lähteet."
    print(f"\n💬 Kysymys: {question}")
    response = app.query(question)

    if args.file:
        with open(args.file, "w", encoding="utf-8") as f:
            f.write(response)
        print(f"\n✅ Vastaus tallennettu tiedostoon: {args.file}")
    else:
        print("\n🧠 Vastaus:")
        print(response)

if __name__ == "__main__":
    main()
