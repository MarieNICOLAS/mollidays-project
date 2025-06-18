FROM python:3.11-slim

WORKDIR /app/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["sh", "-c", "python3 wait_for_db.py && python3 manage.py migrate && python3 scripts/seed_all.py && python3 manage.py runserver 0.0.0.0:8000"]
