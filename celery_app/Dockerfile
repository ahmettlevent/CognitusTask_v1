FROM python:3.6.9
RUN mkdir /usr/src/celery_app
RUN mkdir /usr/src/tmp
WORKDIR /usr/src/celery_app
COPY ./requirements.txt .
RUN pip install -r requirements.txt 
COPY . .
WORKDIR /usr/src/
