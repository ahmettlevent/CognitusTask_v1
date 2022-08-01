FROM python:3.6.9
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt 
COPY . .