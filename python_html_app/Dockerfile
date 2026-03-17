FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5050
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed_marketplace && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT}"]
