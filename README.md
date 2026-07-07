# Трек "Фабрика гипотез"
## Хакатон "Норникель AI SCIENCE HACK"
### Запуск:
```
docker-compose up
```
### Описание:
Платформа для генерации гипотез для НИОКР на основании данных из загруженных вами файлов. Используется ИИ-агент, основанный на Ollama Deepseek-R1 7B.
Используются:
* FastAPI;
* Smolagents;
* Ollama;
* Qdrant;
* SQLAlchemy;
* PostgreSQL;
* JavaScript + HTML + CSS;
* Nginx.
### API:
#### Запрос:
```
GET /api/projects/ - возвращает все проекты.
```
Пример ответа:
```
[
  {
    "id": number,
    "title": string,
    "files": [
      {
        "id": number,
        "title": string
      },
      {
        "id": number,
        "title": string
      }
    ],
    "requests": [
      {
        "id": number,
        "task": string,
        "limitations": string,
        "response": string
      }
    ]
  },
  ...
]
```
#### Запрос:
```
GET /api/projects/{id} - возращает конкретный проект.
```
Пример ответа:
```
{
  "id": number,
  "title": string,
  "files": [
    {
      "id": number,
      "title": string
    },
    {
      "id": number,
      "title": string
    }
  ],
  "requests": [
    {
      "id": number,
      "task": string,
      "limitations": string,
      "response": string
    }
  ]
}
```
#### Запрос:
```
POST /api/projects/add
```
Пример запроса:
```
{
  "title": string
}
```
Пример ответа:
```
Допишу потом
```
