
FROM ubuntu:14.04

RUN sudo apt-get update && apt-get -y install python-pip libpq-dev python-dev

RUN sudo pip install flask==0.10.1 redis

ADD / /code/

WORKDIR /code

EXPOSE 5000

CMD ["python", "app.py"]
