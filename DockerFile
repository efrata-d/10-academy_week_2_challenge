FROM python:3.8-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./scripts /app
COPY ./data /app/data
COPY ./notebooks /app/notebooks

