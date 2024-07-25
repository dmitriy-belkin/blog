# Используйте официальный образ Python
FROM python:3.12-slim

# Установите зависимости
WORKDIR /app

# Скопируйте файлы проекта
COPY . .

# Установите зависимости проекта
RUN pip install --no-cache-dir -r requirements.txt

# Укажите команду для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
