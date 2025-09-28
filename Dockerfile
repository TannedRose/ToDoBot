FROM python:3.11-slim

WORKDIR /app

COPY ./app /app/app
COPY ./bot /app/bot
COPY requirements.txt /app

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "app.wsgi:application", "--chdir", "/app", "--bind", "0.0.0.0:8000"]
