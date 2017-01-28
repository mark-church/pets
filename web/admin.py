from flask import Flask, render_template, request, make_response, redirect
import random, socket, time, json, os, sys, ast, consul

db = os.getenv('DB')
debug = os.getenv('DEBUG', False)
admin_password_file = os.getenv('ADMIN_PASSWORD_FILE')

if admin_password_file is not None:
    f = open(admin_password_file, 'r')
    password = f.readline().rstrip()

app = Flask(__name__)

images = ["https://bloglaurel.com/uploads/2015/10/blog-docker-bloglaurel-ghd-square.jpg"]

url = random.choice(images)

@app.route('/', methods=['GET', 'POST'])
def index():
    admin_id = request.cookies.get('admin_id')

    if admin_id:
        #check if admin_id is valid
        #if not valid then break
        return redirect('/admin')
    
    if admin_password_file is None:
        #set and store admin_id
        return redirect('/admin')
    else: 
        error = None
        if request.method == 'POST':
            if request.form['password'] != password:
                error = 'Invalid credentials.'
            else:
                #set admin_id and store admin_id
                return redirect('/admin')
        return render_template('login.html', error=error, url=url)


@app.route('/admin')
def console():
    return 'SUCCESS'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=debug)
