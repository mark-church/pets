from flask import Flask, render_template, request, make_response
import random, socket, time, json, os, sys, ast, consul

db = os.getenv('DB')
debug = os.getenv('DEBUG')

if debug is None:
    debug = False


container_hostname = socket.gethostname()

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


@app.route('/')
def index():
    return "admin page"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=debug)
