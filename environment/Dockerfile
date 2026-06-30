FROM python:3.11-slim-bookworm@sha256:721dc13fd1be0a771e54b72097634291d628d0007dee9da777e2ce676a9c998f

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-ctrf==0.3.5

WORKDIR /app

COPY access.log /app/access.log
