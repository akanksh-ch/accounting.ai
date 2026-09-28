import os

from openai import OpenAI


def chat(prompt: str) -> str:
    """Send a prompt to Ollama using the OpenAI chat API."""
    with OpenAI(
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1/"),
        api_key="ollama",  # Required by the SDK; ignored by local Ollama.
    ) as client:
        response = client.chat.completions.create(
            model=os.getenv("OLLAMA_MODEL", "granite4.2:8b"),
            messages=[
                {"role": "system", "content": "You are a helpful accounting assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content or ""


if __name__ == "__main__":
    print(chat("Classify Cash as asset, liability, capital, revenue, or expenses."))
