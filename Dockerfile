FROM python:3.11

WORKDIR /app

COPY ./req.txt /app/req.txt

RUN pip install -r req.txt
