FROM python:3.8.10

COPY . .

WORKDIR /app/backend

RUN apt-get update && apt-get install build-essential
RUN make requirements

COPY . /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
