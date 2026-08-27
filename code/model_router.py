# model_router.py #
import os


def chat_client():
    provider = os.getenv("MODEL_PROVIDER", "ollama")
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model="llama3.2", temperature=0), "ollama/llama3.2"
    # using openrouter which is OpenAI compatible:
    from langchain_openai import ChatOpenAI

    return (
        ChatOpenAI(
            model="meta-llama//llama-3.1-8b-instruct",
            base_url="https://openrouter.ai.api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        ),
        "openrouter/llama-3.1-8b",
    )


if __name__ == "__main__":
    client, label = chat_client()
    print(label, "->", client.invoke("Say hi in one word").content)
