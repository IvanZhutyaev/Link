FROM python:3.11

WORKDIR /app

COPY backend/ /app/backend/
COPY requirements.txt /app/
COPY backend/.env /app/backend/.env

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]