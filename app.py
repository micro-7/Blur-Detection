

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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
       
        if email:
            if password:
                print("Email =>", email)
                print("Password =>", password)
                try:
                    db = open_db()
                    user = db.query(User).filter_by(email=email,password=password).first()
                    print(user)
                    if user:
                        session['isauth'] = True
                        session['email'] = user.email
                        session['id'] = user.id
                        del db
                        flash('login successfull','success')
                        return redirect('/')
                    else:
                        flash('email or password is wrong','danger')
                except Exception as e:
                    flash(e,'danger')
                    print(e)
            else:
                print("error")
        else:
            print('email error')
                
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        print(username,email,password,cpassword)

        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(cpassword) == 0:
          flash("All fields are required", 'danger')
          return redirect('/register')
        user = User(username=username,password=password,email=email)
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 