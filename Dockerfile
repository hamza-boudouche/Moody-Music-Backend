# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /moody-music-backend

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt

RUN pip uninstall  bcrypt cffi pycparser
RUN pip install --user --upgrade cffi
RUN pip install --user --upgrade bcrypt
RUN pip install -r ./requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY . .

RUN flask db init ; exit 0
RUN flask db migrate ; exit 0
RUN flask db upgrade ; exit 0

CMD [ "flask", "run"]
