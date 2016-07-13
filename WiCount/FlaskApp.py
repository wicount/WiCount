from flask import Flask, render_template, request, url_for, redirect,session,flash
from functools import wraps
import sqlite3 as sql
import DataRetrieval
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from sqlalchemy.orm import sessionmaker
from CreateUserDb import *

app = Flask(__name__)
Debug = True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a' 
 
# #Login required decorator
# def login_required(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return f(*args,**kwargs)
#         else:
#             return redirect(url_for(home))
#     return wrap


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!  <a href='/logout'>Logout</a>"
 

@app.route('/login', methods=['POST'])
def do_admin_login():
 
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


# To display log out page
@app.route('/logout')
# @login_required
def logout():
    session.pop('logged_in',None)
    return render_template('logout.html')

#To display the map of buildings
@app.route('/campusmap')
#@login_required
def campusMap():
    return render_template('campusmap.html')

#To display the floor plan of rooms
@app.route('/floorplancsi')
#@login_required
def floorPlanCsi():
    return render_template('floorplancsi.html')

#To display the statistics for each room
@app.route('/statsforroom')
#@login_required
def statsForRoom():
    return render_template('statsforroom.html')

#Page to add user
@app.route('/adduser')
#@login_required
def addUser():
    return render_template('adduser.html')

#Page to upload files
@app.route('/fileupload')
#@login_required
def fileUpload():
    return render_template('fileupload.html')

#Page to display statistics
@app.route('/statistics')
#@login_required
def statistics():
    return render_template('statistics.html')

#To display lecturer app page
@app.route('/lecturerapp')
#@login_required
def lecturerApp():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('lecturerapp.html')
#     #return 0
#     json_data = DataRetrieval.getAllCampusDetails()
#     return render_template('lecturerapp.html', CampusDetails = json_data)

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(), validators.Length(min=3, max=35)])
 
 
@app.route("/register", methods=['GET', 'POST'])
def hello():
    
    form = ReusableForm(request.form)
    
    print (form.errors)
    if request.method == 'POST':
        name=request.form['name']
        password=request.form['password']
        email=request.form['email']
        role=request.form['role']
        Session = sessionmaker(bind=engine)
        session = Session()
        user = User(name,password,email,role)
        session.add(user)
        
 
        if form.validate():
            # Save the comment here.
            flash('Thanks for registration ' + name)
            session.commit()
        else:
            flash('Error: All the form fields are required. ')
 
    return render_template('adduser.html', form=form)

if __name__ == '__main__':
    app.run(debug = True)