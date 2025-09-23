from tavily import TavilyClient
import os
import requests

# API-avaimet ympäristömuuttujista
tavily_api_key = os.getenv("TAVILY_API_KEY")
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

tavily_client = TavilyClient(api_key=tavily_api_key)

# Käyttäjän syötteet
hakusana = input("Anna hakusana tai kategoria: ")
aikavali_input = input("Anna aikaväli (tänään, viime viikko, viime kuukausi, viime vuosi): ")

# Muunna käyttäjän syöte oikeaan muotoon
aikavali_map = {
    "tänään": "day",
    "viime viikko": "week",
    "viime kuukausi": "month",
    "viime vuosi": "year",
    "day": "day",
    "week": "week",
    "month": "month",
    "year": "year"
}

aikavali = aikavali_map.get(aikavali_input.strip().lower())

if not aikavali:
    print("Virheellinen aikaväli. Käytä annettuja vaihtoehtoja.")
    exit()

# Hae uutiset
query = f"{hakusana} news"
response = tavily_client.search(query, time_range=aikavali, search_depth="basic", max_results=5)

uutiset = []
for result in response['results']:
    uutiset.append(result['title'] + ": " + result['content'])

uutisteksti = "\n\n".join(uutiset)

# Tiivistä uutiset OpenRouterilla
endpoint = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {openrouter_api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "Tiivistä nämä uutiset suomeksi."},
        {"role": "user", "content": uutisteksti}
    ]
}
response = requests.post(endpoint, headers=headers, json=data)
summary = response.json()["choices"][0]["message"]["content"]

print("\nUutisten tiivistelmä:\n")
print(summary)