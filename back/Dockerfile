FROM python:3.11.10-slim-bullseye

WORKDIR /messenger

# Копируем зависимости
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект, включая main.py в корне
COPY . .

EXPOSE 8000

# Запуск main.py с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# rm -rf messenger_chat
# git clone https://github.com/Varvara168/messenger_chat
# cd messenger_chat
# chmod 644 front/*.html front/*.css front/*.png
# chmod -R 755 front
# docker compose down
# docker compose up -d --build
