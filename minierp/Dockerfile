FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir django djangorestframework psycopg2-binary

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]