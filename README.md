## Инструкция по запуску проекта:

1. Создаие .env в корневой папке и bet-maker, использовать .env.sample для примера
2. Сборка Docker файла
```
docker compose build
```
3. Поднимаем все контейнеры
```
docker compouse up
```

4. Применяем миграции Alembic:
```
alembic upgrade head
```

5. Для доступа к ставкам необходимо получить токен:

# Guide

Создание юзера: http://localhost:8002/api/v1/signup

Получение токена: http://localhost:8002/api/v1/login


