FROM python:3.8.10

COPY . .

WORKDIR /app/frontend

RUN apt-get update && apt-get install build-essential
RUN make requirements

COPY . /app/backend

CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.headless", "true"]
