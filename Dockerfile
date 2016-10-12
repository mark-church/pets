
FROM ubuntu:14.04

RUN sudo apt-get update && apt-get -y install python-pip libpq-dev python-dev curl

RUN sudo pip install flask==0.10.1 redis

ADD / /code/

WORKDIR /code

HEALTHCHECK --interval=1m --timeout=10s CMD curl http://localhost:5000 || exit 1

EXPOSE 5000

CMD ["python", "app.py"]
