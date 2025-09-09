
import openai
import argparse
import os

# Set OpenRouter API key and base URL
client = openai.OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Choose a model available on OpenRouter
MODEL_NAME = "deepseek/deepseek-chat-v3.1:free"

def generate_creative_content(prompt, n_versions=3):
    responses = []
    for version in range(n_versions):
        print(f"\n--- Streaming Version {version + 1} ---\n")
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": (
                    "You are a creative writer who specializes in marketing materials, memes, song lyrics, poems, and blog posts. "
                    "Make the content SEO-optimized by using as many synonyms and keyword variations as possible. "
                    "Be imaginative, engaging, and unique."
                )},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,
            max_tokens=800,
            stream=True
        )

        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                full_response += text
        print("\n")  # Add spacing between versions
        responses.append(full_response.strip())
    return responses

def main():
    parser = argparse.ArgumentParser(description="Creative Writer using OpenRouter API with Streaming")
    parser.add_argument("prompt", type=str, help="Prompt for the creative content")
    parser.add_argument("--versions", type=int, default=3, help="Number of versions to generate")
    args = parser.parse_args()

    print(f"\n🔮 Generating {args.versions} creative versions for:\n\"{args.prompt}\"\n")
    generate_creative_content(args.prompt, args.versions)

if __name__ == "__main__":
    main()
