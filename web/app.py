from flask import Flask, render_template, request
import random, socket, time, json, os, sys, ast, consul

db = os.getenv('DB')
role = os.getenv('ROLE')

if role is None:
    role = 'dog'

healthy = True
version ='2.0'
container_hostname = socket.gethostname()

sys.stdout.write("Starting web container")

app = Flask(__name__)

if db:

    if ':' in db:
        (address, port) = db.split(':')
    else:
        address = db
        port = 8500
        db = address + ':' + str(port)

    time.sleep(10)
    c = consul.Consul(host=address, port=port)
    if c.kv.get('hits')[1] == None:
        c.kv.put('hits', '0')

if (os.path.isfile('/run/secrets/consul-ca.cert') & os.path.isfile('/run/secrets/consul.cert') & os.path.isfile('/run/secrets/consul.key')):
    secured = True

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
    if healthy:
        url = random.choice(images)
    else:
        url = "../static/danger.png"
    
    if db:
        x, hits = c.kv.get('hits')
        newHits = int(hits["Value"]) + 1
        c.kv.put('hits', str(newHits))
        hit_string = str(newHits) + " hits for the " + title + "!"
    if not db:
        hit_string = ""

    return render_template('index.html', url=url, hostname=container_hostname, hit_string=hit_string, title=title, version=version)

@app.route('/health', methods=['GET', 'PUT'])
def health():
    global healthy
    if request.method == 'GET':
        if healthy:
            return 'OK', 200
        else:
            return 'NOT OK', 500
    elif request.method == 'PUT':
        if request.headers['Content-Type'] == 'application/json':
            healthy = ast.literal_eval(str(request.json["healthy"]))
            if healthy == True:
                return "healthy"
            if healthy == False:
                return "not healthy"
    else:
        return 'ERROR REQUEST MTHD', 500

#curl -X PUT -H 'Content-Type: application/json' -d '{"healthy": "False"}' http://localhost:5000/health
#curl -X PUT -H 'Content-Type: application/json' -d '{"healthy": "True"}' http://localhost:8000/health
#curl -v http://localhost:8000/health

if __name__ == "__main__":
    app.run(host="0.0.0.0")
