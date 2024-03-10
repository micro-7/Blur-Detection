

from flask import Flask, render_template,redirect,request, flash, session
from database import User, add_to_db, File, open_db
import os
from werkzeug.utils import secure_filename
from common.file_utils import *


app = Flask(__name__)
app.secret_key = 'thisissupersecretkeyfornoone'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST']) # use froute
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("Email =>", email)
        print("Password =>", password)
        #logic
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST']) # use froute
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        print(username, email, password, cpassword)
        # logic
        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(cpassword) == 0:
            flash("All fields are required", 'danger')
            return redirect('/register') # reload the page
        user = User(username=username, email=email, password=password)
        add_to_db(user)
    return render_template('register.html')

@app.route('/file/upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        name = secure_filename(file.filename)
        path = upload_file(file, name)
        file = File(path=path, user_id=1)
        add_to_db(file)
        flash("File uploaded successfully", 'success')
    return render_template('upload.html')

@app.route('/file/list', methods=['GET','POST'])
def view_files():
    db = open_db()
    files =  db.query(File).all()
    # segregate file into different file types
    fileList = []
    for file in files:
        file = file.__dict__
        file['type'] = os.path.splitext(file['path'])[1]
        print(file)
        fileList.append(file)
    return render_template('display_list.html', files=fileList)

@app.route('/file/<int:id>/view/')
def file_view(id):
    return render_template('view_file.html')

@app.route('/dashboard')
def dashboard():
    #code
    return render_template('dashboard.html')

@app.route('/about')
def about():
    #code
    return render_template('about.html')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 