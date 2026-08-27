# model_router.py #
import os


def chat_client():
    provider = os.getenv("MODEL_PROVIDER", "ollama")
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(model="llama3.2", temperature=0), "ollama/llama3.2"
    # opencode Go which is OpenAI-compatible (flat $10/mo subscription):
    from langchain_openai import ChatOpenAI

    return (
        ChatOpenAI(
            model="deepseek-v4-flash",
            base_url="https://opencode.ai/zen/go/v1",
            api_key=os.getenv("OPENCODE_API_KEY"),
        ),
        "opencode-go/deepseek-v4-flash",
    )


if __name__ == "__main__":
    client, label = chat_client()
    print(label, "->", client.invoke("Say hi in one word").content)
