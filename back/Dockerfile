FROM python:3.11.9-slim

WORKDIR /messenger/back

COPY requirements.txt .
COPY ../main.py .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "/messenger/main.py"]
