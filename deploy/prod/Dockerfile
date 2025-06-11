FROM python:3.10-slim
WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY . .
RUN rm -rf deploy
RUN mv .env.prod .env

EXPOSE 8000
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "server:app", "--bind", "0.0.0.0:8000"]

