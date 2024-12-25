# Глоссарий терминов ВКР

## Описание проекта
Проект представляет собой веб-приложение для управления глоссарием терминов, состоящее из REST API backend'а на FastAPI. Приложение позволяет создавать, читать, обновлять и удалять термины (CRUD операции).

## Технологический стек

### Backend
- Python 3.9
- FastAPI (веб-фреймворк)
- SQLAlchemy (ORM)
- Pydantic (валидация данных)
- Alembic (миграции БД)
- SQLite (база данных)
- uvicorn (ASGI сервер)

### Инфраструктура
- Docker
- Docker Compose

## Функциональность
- Создание новых терминов с определениями и источниками
- Просмотр списка всех терминов
- Поиск терминов
- Редактирование существующих терминов
- Удаление терминов
- Автоматическая генерация API документации (Swagger UI)

## Развертывание

1. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции:
```bash
alembic upgrade head
```

5. Запустите backend:
```bash
uvicorn app.main:app --reload
```

### Запуск через Docker

1. Убедитесь, что Docker и Docker Compose установлены

2. Соберите и запустите контейнеры:
```bash
docker-compose up --build
```

После запуска приложение будет доступно:
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs


## API Endpoints

### Термины
- `GET /terms/` - получить список всех терминов
- `GET /terms/{term_id}` - получить конкретный термин
- `POST /terms/` - создать новый термин
- `PUT /terms/{term_id}` - обновить существующий термин
- `DELETE /terms/{term_id}` - удалить термин

## Разработка

### Backend
Backend использует FastAPI для создания REST API и SQLite в качестве базы данных. Для работы с БД используется SQLAlchemy ORM, а для валидации данных - Pydantic.