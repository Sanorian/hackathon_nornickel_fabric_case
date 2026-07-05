import openai
import requests

import os

YANDEX_FOLDER_ID = os.getenv('YC_FOLDER_KEY')
YANDEX_API_KEY = os.getenv('YC_API_KEY')
YANDEX_MODEL = "aliceai-llm"
OLLAMA_BASE = 'http://ollama:11434'
EMBED_MODEL = 'nomic-embed-text'

def load_llm_client():
    return openai.OpenAI(
    api_key=YANDEX_API_KEY,
    project=YANDEX_FOLDER_ID,
    base_url="https://ai.api.cloud.yandex.net/v1"
)

def embed(text):
    response = requests.post(
        f"{OLLAMA_BASE}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return response.json()['embedding']

def make_request(task, limitations, collection_name, client, qdrant):
    from vector_storage import get_data_from_the_collection

    hits = get_data_from_the_collection(task, collection_name, qdrant)
    knowledges = "\n\n".join(hit.payload['text'] for hit in hits.points)
    prompt = f"""
    Ты - ассистент по генерации гипотез для научно-исследовательских и опытно-конструкторских работ.
    Не используй markdown разметку в своих ответах.
    Сгенерируй гипотезы и отранжируй по приоритетности по задаче:
    {task}
    Ограничения:
    {limitations}
    Используй базу знаний:
    {knowledges}
    """
    response = client.responses.create(
        model=f"gpt://{YANDEX_FOLDER_ID}/{YANDEX_MODEL}",
        input=prompt
    )

    return response.output[0].content[0].text