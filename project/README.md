# SimaLandTask
## Инструкция по запуску:
### 1. ```python3 -m venv venv```
### 2. ```source venv/bin/activate```
### 3. ```pip install -r requirements.txt```
### 4. Переходим в папку core и делаем миграции: 
###              ```alembic revision — autogenerate -m “First commit”```
###              ```alembic upgrade head```
### 5. Переходим в корень проекта и запускаем проект: ```python3 main.py```


# Важно: Тестировал на Ubuntu 22.04
