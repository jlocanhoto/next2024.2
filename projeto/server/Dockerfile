FROM python:3.13-slim

RUN apt-get update && apt-get install -y python3-dev g++ libpq-dev gcc unixodbc unixodbc-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN mkdir -p /app

COPY . /server

CMD ["fastapi", "dev", "/server/app/app.py", "--host=0.0.0.0"]
