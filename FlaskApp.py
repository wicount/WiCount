#import sys
#sys.path.insert(0, "/home/student/anaconda3/lib/python3.4/site-packages")

from flask import Flask, render_template, request, url_for, redirect,session,flash,send_from_directory
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from sqlalchemy.orm import sessionmaker
from passlib.hash import sha256_crypt
from werkzeug import secure_filename
from flask_mail import Mail, Message
from functools import wraps
from CreateUserDb import *
import sqlite3 as sql
import DataRetrieval    
import os
import statisticspy
from werkzeug.security import check_password_hash

app = Flask(__name__)

#Set the debug logs
Debug = True

#Random secret key to set up the application
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

#App configuration for sending email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ucd.wicount@gmail.com'
app.config['MAIL_PASSWORD'] = 'Wicount2016'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail=Mail(app)

#App configuration for uploading files
app.config.from_object(__name__)
app.config['SURVEY'] = 'Survey/'
app.config['TIMETABLE'] = 'timetable/'
app.config['CSILogs'] = 'CSILogs/'
app.config['ALLOWED_EXTENSIONS'] = set(['csv','xlsx']) 
    
# Decorator to make the web pages required login - @login_required
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return index()
    return wrap

def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['role'] == 'admin':
            return f(*args,**kwargs)
        else:
            return index()
    return wrap

#Render login page
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        #Go to Campus Map page if login is successful
        json_data = DataRetrieval.getAllCampusDetails()
        return render_template('campusmap.html',CampusDetails = json_data)
    
#Login request        
@app.route('/login', methods=['POST'])
def login():
    #Fetch login form data and store it in a variable
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])


    #Create a session
    Session = sessionmaker(bind=engine)
    s = Session()
    try:
        #Make the query with database against the form data
        query = s.query(User).filter(User.username.in_([POST_USERNAME]))
        result = query.first()
        if (sha256_crypt.verify(POST_PASSWORD, result.password)) :
            #Set session to true if login is successful
            session['logged_in'] = True
            #velda add user type
            session['role'] = result.role
            session['user'] = result.username
        else:
            flash('Invalid Credentials. Please try again')    
    except:
        #Display error message if login is unsuccessful
        flash('Invalid Credentials. Please try again')    
    #Return to home page
    return index()

#To logout from all pages
@app.route('/logout')
@login_required
def logout():
    #Terminate the session
    session.pop('logged_in',None)
    #Render logout page
    return render_template('logout.html')

#Class to take form input for user registration and user sign up
class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required(),validators.Length(min=4, max=35)])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=6, max=35)])

class SimpleForm(Form):
    name = TextField('Name:', validators=[validators.required(),validators.Length(min=4, max=35)])

class SimplestForm(Form):
    oldpassword = TextField('Existing Password:', validators=[validators.required(), validators.Length(min=6, max=35)])
    newpassword = TextField('New Password:', validators=[validators.required(), validators.Length(min=6, max=35)])
    confirmpassword = TextField('Confirm Password:', validators=[validators.required(), validators.Length(min=6, max=35)])

#User registration by admin 
@app.route("/adduser", methods=['GET', 'POST'])
@admin_login_required
def addUser():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        #Creating session for user registration to send form data to database
        Session = sessionmaker(bind=engine)
        session = Session()
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        role=request.form['role']
        #Pass the form data to user database
        user = User(name,password,email,role)
        #Add user to the session
        session.add(user)
        if form.validate():
            try:
                session.commit()
            except Exception as e:
                session.rollback()
                print(e)
            finally:
                return sendEmailAdmin(name, password, email)
        else:
            #display error message in case of incorrect form data
            flash('Error: All the form fields are required OR Enter correct email address ')
    return render_template('adduser.html', form=form)

#User modification by admin
@app.route("/moduser", methods=['GET', 'POST'])
@admin_login_required
def modUser():
    form = SimpleForm(request.form)
    if request.method == 'POST':
        #Creating session for user registration to send form data to database
        Session = sessionmaker(bind=engine)
        sess = Session()
        name=request.form['name']
        role=request.form['role']

        #Query for user records
        myuser = sess.query(User).filter_by(username=name).first()
        #Add user to the session

        myuser.role = role

        sess.add(myuser)
        if form.validate():
            try:
                sess.commit()
            except Exception as e:
                sess.rollback()
                print(e)
            finally:
                return sendEmailChange(name, role, myuser.email)
        else:
            #display error message in case of incorrect form data
            flash('Error: All the form fields are required OR Enter correct email address ')
    return render_template('moduser.html', form=form)

#User modification by user
@app.route("/chguser", methods=['GET', 'POST'])
@login_required
def chgUser():
    form = SimplestForm(request.form)
    if request.method == 'POST':
        #Creating session for user registration to send form data to database
        Session = sessionmaker(bind=engine)
        sess = Session()
        name=session['user']
        oldpassword=request.form['oldpassword']
        newpassword=request.form['newpassword']
        confirmpassword=request.form['confirmpassword']

        #Query for user records
        myuser = sess.query(User).filter_by(username=name).first()
        #Add user to the session

        if sha256_crypt.verify(oldpassword, myuser.password) and newpassword == confirmpassword:

            myuser.password = sha256_crypt.encrypt(newpassword)

            sess.add(myuser)
            if form.validate():
                try:
                    sess.commit()
                except Exception as e:
                    sess.rollback()
                    print(e)
                finally:
                    return sendEmailPassword(name, myuser.email)
            else:
                #display error message in case of incorrect form data
                flash('Error: All the form fields are required OR Enter correct email address ')
        else:
            flash('Error: Ensure that you have entered your existing password correctly and that the new password has been entered correctly')
    return render_template('chguser.html', form=form)

#User registration by end user
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = ReusableForm(request.form)
    if request.method == 'POST':
        #Creating session for user registration to send form data to database
        Session = sessionmaker(bind=engine)
        session = Session()
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        role = 'enduser'
        #Pass the form data to user database
        user = User(name,password,email,role)
        #Add user to the session
        session.add(user)
        if form.validate():
            #Commit user data to database
            try:
                session.commit()                
            except Exception as e:
                session.rollback()
                print(e)
            finally:
                return sendEmail(name,password,email)
        else:
            #display error message in case of incorrect form data
            flash('Error: All the form fields are required OR Enter correct email address ')
    return render_template('signup.html', form=form)

#To send email for the registered users
@app.route("/sendemail")
def sendEmail(name,password,email):
    msg = Message('WiCount - Username and Password', sender = 'rakesh.bt1990@gmail.com', recipients = [email])
    msg.body = "Please use following credentials to login \n\n username: %s\nPassword: %s  " % (name,password )
    mail.send(msg)
    return render_template('email.html')

@app.route("/sendemailadmin")
@admin_login_required
def sendEmailAdmin(name,password,email):
   msg = Message('WiCount - Username and Password', sender = 'ucd.wicount@gmail.com', recipients = [email])
   msg.body = "Please use following credentials to login \n\n username: %s\nPassword: %s  " % (name,password )
   mail.send(msg)
   return render_template('emailadmin.html')

@app.route("/sendemailchange")
@admin_login_required
def sendEmailChange(name,role,email):
   msg = Message('WiCount - You have been granted additional access', sender = 'ucd.wicount@gmail.com', recipients = [email])
   msg.body = "\n%s is now assigned the role of %s  " % (name,role)
   mail.send(msg)
   return render_template('emailchange.html')

@app.route("/sendemailpassword")
@admin_login_required
def sendEmailPassword(name, email):
   msg = Message('WiCount - Password Change Notification', sender = 'ucd.wicount@gmail.com', recipients = [email])
   msg.body = "\n%s your password has been changed. Please reply if you have not changed the password" % (name)
   mail.send(msg)
   return render_template('emailpassword.html')

#Initial file upload template
@app.route('/fileupload')
@admin_login_required
def fileupload():
    return render_template('fileupload.html')

#For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

#Route that will process the file upload
@app.route('/upload', methods=['POST'])
@admin_login_required
def upload():
    # Get the name of the uploaded files
    uploaded_files1 = request.files.getlist("survey")
    uploaded_files2 = request.files.getlist("timetable")
    uploaded_files3 = request.files.getlist("log")
    filenames = []
    for file in uploaded_files1:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['SURVEY'], filename))
            filenames.append(filename)
            flash('Files Uploaded Successfully')
    for file in uploaded_files2:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['TIMETABLE'], filename))
            filenames.append(filename)
            flash('Files Uploaded Successfully')
    for file in uploaded_files3:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['CSILogs'], filename))
            filenames.append(filename)
            flash('Files Uploaded Successfully')
    return render_template('fileupload.html')

#To display the map of buildings
@app.route('/campusmap')
@login_required
def campusMap():
    json_data = DataRetrieval.getAllCampusDetails()
    return render_template('campusmap.html',CampusDetails = json_data)


#To display the floor plan of rooms
@app.route('/floorplancsi')
@login_required
def floorPlanCsi():
    return render_template('floorplancsi.html')

#To display the statistics for each room
@app.route('/statsforroom')
@login_required
def statsForRoom(room_id=None):
#     return render_template('statsforroom.html')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        print(request.method)
        print(request.args.get('room_id'))
        if request.method == 'GET':
            room_id=request.args.get('room_id')
        else:
            room_id=request.form['room'] 
        roomsInBuilding = DataRetrieval.GetBuildingDetails(room_id)
        surveyData = DataRetrieval.StatsForRoom(room_id)
        return render_template('statsforroom.html', BuildingDetails = roomsInBuilding, room_id = room_id, surveyData = surveyData)

#To display lecturer app page
@app.route('/lecturerapp', methods=['GET', 'POST'])
@login_required
def lecturerApp():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            room_id=request.form['room']
            percent=request.form['percent']
            day=request.form['day']
            time=request.form['time']
            message = DataRetrieval.createSurveyFile(room_id, percent, day, time)
        else:
            message = ""
        json_data = DataRetrieval.getAllCampusDetails()
        return render_template('lecturerapp.html', CampusDetails = json_data, message = message)
    
#Page to display statistics
@app.route('/statistics',methods=['GET', 'POST'])
#@login_required
def statistics():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'GET':
            room = request.args.get('category2')
            occupancy = request.args.get('category2')
            results = statisticspy.percentage_utilisation(room)
            results2 = statisticspy.list_occupancy_x(occupancy)
        else:
            results = ""
        
        return render_template('statistics.html', results = results,results2 = results2)
if __name__ == '__main__':
    app.run(debug = True)
