FROM python:3.7-slim

WORKDIR /home

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt && rm ./requirements.txt

