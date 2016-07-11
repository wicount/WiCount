'''
Created on 28 Jun 2016

@author: Rakesh Lakshman
'''
from flask import Flask, render_template, request, url_for, redirect,session,flash
from functools import wraps
import sqlite3 as sql

app = Flask(__name__)

#Session Secret Key
app.secret_key = "wicount"
  
#Login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            return redirect(url_for(login))
    return wrap

# To display login page
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == 'admin' or request.form['password'] == 'admin':
            session['logged_in'] = True
            flash('logged in')
            return redirect(url_for('buildingmap'))
        elif request.form['username'] == 'user' or request.form['password'] == 'user':
            session['logged_in'] = True
            flash('logged in')
            return redirect(url_for('buildingmap'))  
        else:
            error = 'Invalid Credentials. Please try again.'    
    return render_template('login.html', error=error)

# To display log out page
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in',None)
    return render_template('logout.html')

#To display the map of buildings
@app.route('/campusmap')
#@login_required
def campusMap():
    return render_template('campusmap.html')

#To display the floor plan of rooms
@app.route('/floorplan')
#@login_required
def floorPlan():
    return render_template('floorplan.html')

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
    return 0
    #json_data = DataRetrieval.getAllcampusdetails()
   # return render_template('lecturerapp.html', CampusDetails = json_data)


if __name__ == '__main__':
    app.run(debug = True)