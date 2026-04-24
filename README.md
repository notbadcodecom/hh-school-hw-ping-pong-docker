# Ping-Pong Emulator

## Задание:
1. Написать Dockerfile для сборки проекта (пригодятся команды из раздела "Запуск")
2. Написать docker-compose.yml

## Условия:
1. Данные сохраняем базу, поднятую контейнером
2. Данные должны сохраняться, если контейнеры остановить\запустить
3. Приложение должно открываться и работать

## Требования:
1. Python 3.10+
2. Наличие переменных окружения для подключения к db:
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME=pingpong
- DB_USER=postgres
- DB_PASSWORD=postgres
- DB_HOST=db
- DB_PORT=5432

## Запуск
### mac/linux
```bash
python3 -m .venv venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
### Windows
```bash
python -m .venv venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Открыть http://localhost:8000


## Что дальше?
1. Нажмите кнопку "Сыграть матч"
2. Наблюдайте лог игры в реальном времени
3. Смотрите историю матчей в таблице справа
4. Можете сыграть ещё или очистить историю
