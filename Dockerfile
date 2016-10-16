FROM python:3.5.2-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/

RUN set -x \
    && apt-get update \
    && apt-get install curl -y \
    && curl -sL https://deb.nodesource.com/setup_6.x | bash - \
    && apt-get install \
        vim \
        libffi6 \
        libffi-dev \
        libpq-dev \
        gcc \
        g++\
        make \
        postgresql-client --no-install-recommends \
        nodejs -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -q -r requirements.txt

COPY package.json .
RUN npm install
