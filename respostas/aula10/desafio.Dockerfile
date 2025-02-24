FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

COPY app.py app.py

RUN pip install fastapi[standard]

EXPOSE 8000

CMD ["fastapi", "dev", "app.py", "--host=0.0.0.0"]
