FROM python:3.13-slim

RUN pip install fastapi[standard]

WORKDIR /app

COPY app.py app.py
COPY index.html index.html

ENV PYTHONUNBUFFERED=1

CMD ["fastapi", "dev", "app.py", "--host=0.0.0.0"]
