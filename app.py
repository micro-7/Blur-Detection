

from flask import Flask, render_template, redirect, flash, request #use fapp
from database import User, add_to_db, open_db

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

@app.route('/signup', methods=['GET', 'POST']) # use froute
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("Email =>", email)
        print("Password =>", password)
        #logic
    return render_template('signup.html')

@app.route('/file/upload', methods=['GET', 'POST'])
def file_upload():
    #code
    return render_template('upload.html')

@app.route('/about')
def about():
    #code
    return render_template('about.html')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 