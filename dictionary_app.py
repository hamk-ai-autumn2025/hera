import json
import sys

def generate_entry(word: str) -> dict:
    w = word.strip()
    lw = w.lower()

    examples = {
        "ohjelmointi": {
            "word": "ohjelmointi",
            "definition": "The process of designing, writing, testing, debugging, and maintaining the source code of computer programs.",
            "synonyms": ["koodaus", "sovelluskehitys"],
            "antonyms": [],
            "examples": [
                "Opiskelen ohjelmointia yliopistossa.",
                "Verkkosivun ohjelmointi vaatii HTML:n ja CSS:n osaamista."
            ],
        },
        "kallis": {
            "word": "kallis",
            "definition": "expensive, dear, costly",
            "synonyms": ["hintava", "arvokas", "tyyris"],
            "antonyms": ["halpa", "edullinen"],
            "examples": [
                "Tämä auto on liian kallis.",
                "Hän on minulle hyvin kallis ystävä."
            ],
        },
        "halpa": {
            "word": "halpa",
            "definition": "cheap, inexpensive",
            "synonyms": ["edullinen", "huokea"],
            "antonyms": ["kallis", "hintava"],
            "examples": [
                "Tämä kahvila on todella halpa.",
                "Halpa hinta ei aina tarkoita huonoa laatua."
            ],
        },
        "koulu": {
            "word": "koulu",
            "definition": "An institution for educating children or adults.",
            "synonyms": ["oppilaitos", "opisto"],
            "antonyms": [],
            "examples": [
                "Lapset menevät kouluun kahdeksalta.",
                "Koulu sijaitsee kylän keskustassa."
            ],
        },
        "tietokone": {
            "word": "tietokone",
            "definition": "An electronic device for storing and processing data.",
            "synonyms": ["PC", "kompuutteri", "mikro"],
            "antonyms": [],
            "examples": [
                "Tietokone on välttämätön työkalu nykypäivänä.",
                "Uusi tietokone toimii nopeasti."
            ],
        },
        "kirja": {
            "word": "kirja",
            "definition": "A written or printed work consisting of pages bound together.",
            "synonyms": ["teos", "opas", "julkaisu"],
            "antonyms": [],
            "examples": [
                "Luulin tämän olevan mielenkiintoinen kirja.",
                "Hän kirjoitti ensimmäisen kirjansa vuonna 2010."
            ],
        },
        "nopea": {
            "word": "nopea",
            "definition": "fast, quick, rapid",
            "synonyms": ["vauhdikas", "pikainen"],
            "antonyms": ["hidas"],
            "examples": [
                "Juna on nopea kulkuneuvo.",
                "Hän teki nopean päätöksen."
            ],
        },
        "hidas": {
            "word": "hidas",
            "definition": "slow, sluggish",
            "synonyms": ["verkkaisa", "viipyilevä"],
            "antonyms": ["nopea"],
            "examples": [
                "Liikenne oli tänään hyvin hidasta.",
                "Tämä tietokone on liian hidas."
            ],
        },
    }

    if lw in examples:
        return examples[lw]

    return {
        "word": w,
        "definition": "",
        "synonyms": [],
        "antonyms": [],
        "examples": []
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "word": "",
            "definition": "",
            "synonyms": [],
            "antonyms": [],
            "examples": []
        }, ensure_ascii=False, indent=4))
        return

    word = " ".join(sys.argv[1:])
    entry = generate_entry(word)
    print(json.dumps(entry, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
