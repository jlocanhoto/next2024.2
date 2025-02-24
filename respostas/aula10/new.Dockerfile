FROM next-aula-10:2.0

ENV PYTHONUNBUFFERED=1

COPY main.py main.py

CMD ["python", "main.py"]
