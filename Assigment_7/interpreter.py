import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import time
import os

fs = 44100
sekuntia = 8
filename = "test.wav"

# Kielisanakirja: puhutun nimen ja GoogleTrans/Gtts-koodin välinen yhteys
language_map = {
    "englanti": ("en", "English"),
    "ranska": ("fr", "French"),
    "saksa": ("de", "German"),
    "espanja": ("es", "Spanish"),
    "ruotsi": ("sv", "Swedish")
}

pygame.mixer.init()  # Alusta pygame kerran

def get_target_language():
    while True:
        print("\nSano mille kielelle käännetään (englanti, ranska, saksa, espanja, ruotsi):")
        recording = sd.rec(int(sekuntia * fs), samplerate=fs, channels=1)
        sd.wait()
        sf.write(filename, recording, fs)
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = r.record(source)
        try:
            lang_text = r.recognize_google(audio, language="fi-FI").lower()
            print("Tunnistettu kieli:", lang_text)
            for key in language_map:
                if key in lang_text:
                    return language_map[key][0], language_map[key][1]
            print("Kieltä ei tunnistettu, yritä uudelleen.")
        except Exception as e:
            print("Jokin meni pieleen:", e)

target_lang, target_lang_name = get_target_language()

while True:
    print(f"\nPuhu mikrofoniin ({sekuntia} sekuntia). Käännetään: {target_lang_name}. Sano 'lopeta' lopettaaksesi tai 'vaihda kieli' vaihtaaksesi kieltä.")
    recording = sd.rec(int(sekuntia * fs), samplerate=fs, channels=1)
    sd.wait()
    sf.write(filename, recording, fs)

    r = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language="fi-FI")
        print("Tunnistettu teksti:", text)
    except Exception as e:
        print("Jokin meni pieleen:", e)
        text = ""

    if text:
        if "lopeta" in text.lower():
            print("Lopetetaan ohjelma.")
            break
        if "vaihda kieli" in text.lower():
            target_lang, target_lang_name = get_target_language()
            continue

        translator = Translator()
        translation = translator.translate(text, src='fi', dest=target_lang)
        print(f"Käännös ({target_lang_name}):", translation.text)

        tts = gTTS(translation.text, lang=target_lang)
        tts.save("translation.mp3")
        print(f"Luetaan käännös ääneen ({target_lang_name})...")

        pygame.mixer.music.load("translation.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.5)
        pygame.mixer.music.unload()
        time.sleep(0.1)
        try:
            os.remove("translation.mp3")
        except Exception as e:
            print("Tiedoston poisto epäonnistui:", e)
    else:
        print("Puhetta ei tunnistettu.")
    time.sleep(1)

