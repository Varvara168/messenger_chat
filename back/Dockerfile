FROM python:3.11.9-slim

COPY requirements.txt /messenger/requirements.txt
RUN pip install -r /messenger/requirements.txt

COPY . . /messenger/back

CMD ["python", "/messenger/main.py"]