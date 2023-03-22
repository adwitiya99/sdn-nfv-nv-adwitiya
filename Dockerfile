FROM python:3.8.16-bullseye

RUN apt-get update -y


ENV PYTHONUNBUFFERED 1
WORKDIR /app

EXPOSE 8000

COPY requirement.txt ./requirement.txt
RUN pip install -r requirement.txt
COPY . .
