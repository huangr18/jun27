from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash, Response
from db import load_users_from_db, get_user_firstname_from_db, get_username_from_db, add_video_from_db, get_user,user_register, get_password_from_db, update
from datetime import timedelta
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from aivision import runcv

from test import gen_frames
from video_convert import convert


app = Flask(__name__, static_folder='static')
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(hours=1)
app.config['SECRET_KEY'] = 'hello'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")


#home page

@app.route("/home")
def home():
    return render_template('home.html', company_name='AI Training Center')

#see users
@app.route("/api/get_users")
def api_get_users():
    all_users = load_users_from_db()
    return jsonify(all_users)

@app.route("/api/user")
def api_user():
    user = get_user_firstname_from_db('jimh01@gmail.com')

    return user


#login page
@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form['email']
        submit_password = request.form['password']
        firstname = get_user_firstname_from_db(email)
        username = get_username_from_db(email)
        password = get_password_from_db(email)
        if submit_password == password:
            session["firstname"] = firstname
            session["username"] = username
            return redirect(url_for('user'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route("/user", methods=['GET', 'POST'])
def user():
    if "firstname" in session:
        firstname = session["firstname"]
        username = session["username"]

        user_past_video = get_user(username)
        # for video in user_past_video:
        #     user_past_video = video.get('video_name')
        



        form = UploadFileForm()
        if form.validate_on_submit():
            file = form.file.data
            filename = file.filename
            filename = username + filename
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(filename)))
            add_video = add_video_from_db(username, filename)
            return render_template('upload_success.html', filename=filename, add_video=add_video)
        
        return render_template('user.html', firstname=firstname, form=form, user_past_video=user_past_video)
    else:
        if "firstname" in session:
            return redirect(url_for("user"))
        
        return redirect(url_for("login"))


# @app.route("/video/<filename>", methods=['GET', 'POST'])
# def video(filename):
#     if "firstname" in session:
#         username = session["username"]

#         return Response(runcv(filename), mimetype='multipart/x-mixed-replace; boundary=frame')
#     return render_template('upload_success.html')

@app.route("/video/<filename>", methods=['GET', 'POST'])
def video(filename):
    if "firstname" in session:
        username = session["username"]
        result_filename = runcv(filename)
        timesdone = update(filename, result_filename[1])
        result_filename = result_filename[0]
        result_filename = convert(result_filename)

    
        # result_filename = convert(result_filename)
    return render_template('video.html', username=username, result_filename=result_filename, filename=filename, timesdone=timesdone)

    


@app.route("/logout")
def logout():
    session.pop("firstname", None)
    flash("You have been logout!", "info")
    return redirect(url_for("home"))


@app.route("/api/test")
def api_test():
    filename = 'jimhproduction_id_4438094_1080p'
    return Response(gen_frames(filename), mimetype='multipart/x-mixed-replace; boundary=frame')




# register
@app.route("/register", methods=['GET','POST']) 
def register():
    if request.method == "POST":
        username = request.form['username']
        firstname = request.form['firstname']
        email = request.form['email']
        password = request.form['password']
        status = user_register(username, firstname, email, password)
        return status

    return render_template('register.html')


# history
@app.route("/history", methods=['GET','POST']) 
def history():
    if "firstname" in session:
        username = session["username"]

        user_past_video = get_user(username)
        return render_template('history.html', user_past_video=user_past_video)
    else:
        return redirect(url_for("login"))


# past result
@app.route("/past/<video_name>", methods=['GET','POST']) 
def pastresult_display(video_name):
    if "firstname" in session:
        username = session["username"]

        return render_template('pastresult_display.html', username=username, video_name=video_name)
    else:
        return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug="True")