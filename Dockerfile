# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster



RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install pipenv

COPY requirements.txt .
RUN python3.10 -m pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel
RUN python3.10 -m pip install --no-cache-dir \
    -r requirements.txt

COPY . .

CMD ["./start.sh"]
