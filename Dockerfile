FROM python:3.12-slim

WORKDIR /server_app
COPY server_app/ .

RUN apt-get update && \
    apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr tesseract-ocr-rus && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /server_app/src
RUN pip3 install --no-cache-dir -r requirements.txt -v --timeout=100

EXPOSE 8000/tcp

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]