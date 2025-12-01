# Используем официальный образ Python 3.12
FROM --platform=linux/amd64 python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY src/ .

# Указываем порт, который будет использовать приложение
ENV PORT 8080

# Запускаем приложение
CMD ["python", "main.py"]
