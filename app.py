

from flask import Flask, render_template,redirect,request, flash, session
from database import User, add_to_db, File, open_db
import os
from werkzeug.utils import secure_filename
from common.file_utils import *
from common.blur_vid import process_video  
from common.remove_vid_blur import remove_blur_from_video
from common.image_blur_detection import detect_img_blur


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

@app.route('/file/fixed', methods=['GET','POST'])
def fixed_files():
    db = open_db()  
    processed_files =  db.query(File).all()
    # segregate file into different file types
    fileList = []
    for file in processed_files:
        file = file.__dict__
        file['type'] = os.path.splitext(file['path'])[1]
        print(file)
        fileList.append(file)
    return render_template('fixed_videos.html', files=fileList)

@app.route('/file/<int:id>/view/')
def file_view(id):
    return render_template('view_file.html')

@app.route('/delete/<int:id>')
def delete_file(id):
    db = open_db()
    file = db.query(File).filter_by(id=id).first()
    if file:
        os.remove(file.path)
        db.delete(file)
        db.commit()
        db.close()
        flash("File deleted successfully", 'success')
        return redirect('/file/list')
    return render_template('view_file.html')

@app.route('/blur/vid/<int:id>')
def detect(id):
    db = open_db()
    file = db.query(File).filter_by(id=id).first()
    out = process_video(file.path, 100.0)   
    output_path = remove_blur_from_video(file.path, out, f"videos/{file.id}_blur_removed.mp4")
    print("Output video saved at:", output_path)
    flash("Blur removed successfully", 'success')
    return redirect('/file/list')

@app.route('/blur/img/<int:id>')
def detect_img(id):
    db = open_db()
    file = db.query(File).filter_by(id=id).first()
    print(file)
    is_blurry = detect_img_blur(file.path)
    if is_blurry:
        flash("Image is blurry", 'danger')
        msg = f'Image is blurry, please remove this image{file.path}'
    else:
        flash("Image is not blurry", 'success')
        msg = f'Image is not blurry, {file.path}'
    return render_template('view_file.html', file=file, msg=msg)
    


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
 