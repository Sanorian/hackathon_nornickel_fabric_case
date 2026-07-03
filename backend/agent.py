import openai
import requests

import os

YANDEX_FOLDER_ID = "b1ggusvist6c2sia1dno"
YANDEX_API_KEY = "AQVN34pk7pZhEv_vgD7voZpc76HQt7n5tSce4b_5"
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
    return response.json()['embeddings']

def make_request(task, limitations, collection_name, client):
    from vector_storage import get_data_from_the_collection

    hits = get_data_from_the_collection(task, collection_name)
    knowledges = "\n\n".join(hit.payload['text'] for hit in hits.points)
    prompt = f"""
    Ты - ассистент по генерации гипотез для научно-исследовательских и опытно-конструкторских работ.
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

    return response.output[0].content[0].text, response.output[0].thinking[0].text