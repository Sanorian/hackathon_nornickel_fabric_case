import requests
from smolagents import CodeAgent, DuckDuckGoSearchTool, LiteLLMModel, VisitWebpageTool, tool

import os

OLLAMA_BASE = 'http://ollama:11434'
EMBED_MODEL = 'nomic-embed-text'
LLM = 'deepseek-r1:7b'

def load_model():
    model = LiteLLMModel(
        model_id = f'ollama_chat/{LLM}',
        api_base = OLLAMA_BASE
    )
    return model

def embed(text):
    response = requests.post(
        f"{OLLAMA_BASE}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}
    )
    return response.json()['embedding']

def make_request(task, limitations, collection_name, model, qdrant):
    from vector_storage import get_data_from_the_collection
    
    @tool
    def get_data_from_vector_database(task: str) -> str:
        """
        This is a tool that return
        the 10 most semantically matching data chunks from the knowledge base (vector database).

        Args:
            task: The information for what we loooking in knowledge base
        """
        hits = get_data_from_the_collection(task, collection_name, qdrant)
        knowledges = "\n\n".join(hit.payload['text'] for hit in hits.points)
        return knowledges
    
    agent = CodeAgent(
        tools = [
            DuckDuckGoSearchTool(),
            VisitWebpageTool(),
            get_data_from_vector_database
        ],
        model = model,
        additional_authorized_imports = [
            'requests',
            'bs4'
        ],
        max_steps = 50
    )
    prompt = f"""
    Ты - ассистент по генерации гипотез для научно-исследовательских и опытно-конструкторских работ.
    Не используй markdown разметку в своих ответах.
    Сгенерируй гипотезы и отранжируй по приоритетности по задаче:
    {task}
    Ограничения:
    {limitations}
    Используй базу знаний и поиск в интернете.
    Отвечай на русском.
    """
    response = agent.run(prompt)

    return response