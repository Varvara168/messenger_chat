FROM python:3.11.9-slim

WORKDIR /messenger/back



# Копируем файлы из корня проекта
COPY requirements.txt .
COPY main.py .

# Если есть папка back с кодом
COPY back/ .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["python", "/messenger/back/main.py"]
