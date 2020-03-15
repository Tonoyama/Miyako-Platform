FROM python:3.6

USER root

WORKDIR /app
ADD . /app

COPY . .

RUN apt-get update
RUN apt-get install python3 python3-pip -y
RUN apt-get install build-essential -y
RUN pip3 install Flask requests flask_login xlrd sqlalchemy pymysql

EXPOSE 80

CMD ["python", "app.py"]