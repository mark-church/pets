from flask import Flask, render_template, request
from redis import Redis
from redis.exceptions import ConnectionError
import random, socket, time, json, os, sys

db1 = os.getenv('DB1')
db2 = os.getenv('DB2')

sys.stdout.write("Starting admin container")

app = Flask(__name__)

while True:
    try:
        redis1 = Redis(host=db1, db=0, socket_timeout=5)
        redis1.get(None)
        break
    except ConnectionError:
        sys.stdout.write("Attempting to connect to DB1. Trying again in 3 seconds ...")
        time.sleep(3)

while True:
    try:
        redis2 = Redis(host=db2, db=0, socket_timeout=5)
        redis2.get(None)
        break
    except ConnectionError:
        sys.stdout.write("Attempting to connect to DB2. Trying again in 3 seconds ...")
        time.sleep(3)

@app.route('/')
def index():
    cathits = redis1.llen(db1)
    doghits = redis2.llen(db2)
    return render_template('admin.html', cathits=cathits, doghits=doghits)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
