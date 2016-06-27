'''
Created on 27 Jun 2016

@author: Rakesh Lakshman
'''
from flask import Flask, g, render_template, request
import sqlite3 as sql
app = Flask(__name__)

#Part 1 - Function to connect to the database.
DATABASE = 'wicount.sqlite3'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

        
#Part 2 - To Query the database and get information for data analytics part     
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#Part 3 - Data Analyics
def data_analytics():
    return 0


#Part 4 - Update the results from data analytics into database
def update_db():
    return 0


    
#Part 5 -  Web Side functionalities     
# To display Home Page
@app.route('/')
def homePage():
    return render_template('index.html')

# To display end user home page
@app.route('/enduserpage')
def endUserPage():
    return render_template('endUserPage.html')

# To display Admin home page
@app.route('/adminpage')
def adminPage():
    return render_template('adminPage.html')

# To display the results for end user(Graphs and Charts)
@app.route('/displayresults')
def displayResults():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
   
    cur = con.cursor()
    cur.execute("select * from ")
   
    rows = cur.fetchall();
    return render_template("displayresults.html",rows = rows)

#To display results for admin page
def displayResultsAdmin():
    return 0

if __name__ == '__main__':
    app.run(debug = True)