FROM ubuntu:18.04
RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN apt-get install -y curl python3.6 python3.6-dev python3.6-distutils
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
RUN update-alternatives --set python /usr/bin/python3.6
RUN apt-get update && apt-get -y install python3-pip 
RUN mkdir /app
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt 
COPY . .
CMD [ "python3", "./app.py" ]