from flask import Flask, render_template, request
from redis import Redis
from redis.exceptions import ConnectionError
import random, socket, time, json, os, sys

db = os.getenv('DB')
role = os.getenv('ROLE')

sys.stdout.write("Starting web container")

app = Flask(__name__)

if ':' in db:
    (address, port) = db.split(':')
else:
    address = db
    port = 6379
    db = address + ':' + str(port)

while True:
    try:
        redis = Redis(host=address, port=port, db=0, socket_timeout=5)
        redis.get(None)
        break
    except ConnectionError:
        print "Attempting to connect to %s. Trying again in 3 seconds ..." % db
        time.sleep(3)

container_hostname = socket.gethostname()

if role == 'cat':
    title = "Cats"
    images = [
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26388-1381844103-11.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr01/15/9/anigif_enhanced-buzz-31540-1381844535-8.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26390-1381844163-18.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-1376-1381846217-0.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3391-1381844336-26.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/10/anigif_enhanced-buzz-29111-1381845968-0.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/9/anigif_enhanced-buzz-3409-1381844582-13.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr02/15/9/anigif_enhanced-buzz-19667-1381844937-10.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr05/15/9/anigif_enhanced-buzz-26358-1381845043-13.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-18774-1381844645-6.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr06/15/9/anigif_enhanced-buzz-25158-1381844793-0.gif",
        "http://ak-hdl.buzzfed.com/static/2013-10/enhanced/webdr03/15/10/anigif_enhanced-buzz-11980-1381846269-1.gif"
        ]
elif role == 'dog':
        title = "Dogs"
        images = [
        "https://img.buzzfeed.com/buzzfeed-static/static/2013-12/enhanced/webdr06/3/12/anigif_enhanced-buzz-12996-1386090648-41.gif",
        "https://img.buzzfeed.com/buzzfeed-static/static/2013-12/enhanced/webdr06/3/12/anigif_enhanced-buzz-14140-1386090436-22.gif",
        "https://img.buzzfeed.com/buzzfeed-static/static/2013-12/enhanced/webdr07/3/12/anigif_enhanced-buzz-14182-1386090558-25.gif",
        "https://img.buzzfeed.com/buzzfeed-static/static/enhanced/webdr01/2012/12/15/16/anigif_enhanced-buzz-19342-1355608696-6.gif"
        ]
else:
    sys.stdout.write("Error: no valid role")
    sys.exit(1)


@app.route('/')
def index():
    url = random.choice(images)
    hit = (str(request.environ['REMOTE_ADDR']),time.asctime())
    redis.lpush(db,hit)
    numhits = redis.llen(db)
    return render_template('index.html', url=url, hostname=container_hostname, numhits=numhits, title=title)

@app.route('/hits')
def hits():
    for i in range(0,redis.llen(db)):
        print redis.lindex(db,i)
    return str(json.dumps(redis.llist(db)))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
