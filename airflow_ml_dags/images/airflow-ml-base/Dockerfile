FROM python:3.7-slim

RUN apt update && apt install git -y 

RUN mkdir /build/

COPY requirements.txt /build/requirements.txt

RUN pip install --no-cache -r /build/requirements.txt