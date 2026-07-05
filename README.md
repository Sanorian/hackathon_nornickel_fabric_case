# Трек "Фабрика гипотез"
## Хакатон "Норникель AI SCIENCE HACK"
### Запуск:
Необходимо добавить ```.env``` файл
```
YC_API_KEY=<Ваш API ключ>
YC_FOLDER_ID=<Ваше Folder ID>
```
### Описание:
Платформа для генерации гипотез для НИОКР на основании данных из загруженных вами файлов. Используется Yandex AI Studio API.
Используются:
* FastAPI;
* OpenAI;
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