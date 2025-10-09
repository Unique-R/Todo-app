FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
COPY templates/ ./templates/
COPY tests/ ./tests/

# Оставляем рабочую директорию /app
# и указываем правильный путь к модулю
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]
