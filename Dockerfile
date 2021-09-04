# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /http-hash-server
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY .env .env
COPY http_hash_server.py http_hash_server.py
CMD ["python3", "http_hash_server.py"]