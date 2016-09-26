from flask import Flask, render_template, request
from redis import Redis
from redis.exceptions import ConnectionError
import random, socket, time, json, os, sys

db1 = os.getenv('DB1')
db2 = os.getenv('DB2')

sys.stdout.write("Starting admin container")

app = Flask(__name__)



if ':' in db1:
    (address1, port1) = db1.split(':')
else:
    address1 = db1
    port1 = 6379
    db1 = address1 + ':' + str(port1)

if ':' in db2:
    (address2, port2) = db2.split(':')
else:
    address2 = db2
    port2 = 6379
    db2 = address2 + ':' + str(port2)

while True:
    try:
        redis1 = Redis(host=address1,port=port1, db=0, socket_timeout=5)
        redis1.get(None)
        break
    except ConnectionError:
        sys.stdout.write("Attempting to connect to DB1. Trying again in 3 seconds ...")
        time.sleep(3)

container_hostname = socket.gethostname()

while True:
    try:
        redis2 = Redis(host=address2,port=port2, db=0, socket_timeout=5)
        redis2.get(None)
        break
    except ConnectionError:
        sys.stdout.write("Attempting to connect to DB2. Trying again in 3 seconds ...")
        time.sleep(3)

@app.route('/')
def index():
    cathits = redis1.llen(db1)
    doghits = redis2.llen(db2)
    return render_template('admin.html', cathits=cathits, doghits=doghits, hostname=container_hostname)

@app.route('/health')
def index():
    return 'OK'

if __name__ == "__main__":
    app.run(host="0.0.0.0")
