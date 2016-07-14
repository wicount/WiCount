import sqlite3 as sql
from sqlite3 import OperationalError
import json #used to build json strings
import os
from dateutil.parser import parse
from datetime import datetime, timedelta

def getAllCampusDetails():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row # This enables column access by name: row['column_name'] 
    cur = con.cursor()

    rows = cur.execute('''
    SELECT * FROM room
    ''').fetchall()

    con.commit()
    con.close()
    print ("1: ", json.dumps( [dict(ix) for ix in rows] ))
    return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON


def GetDay(i):
    ''' return the day of the week'''
    return {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
    }.get(i, 1)
    
def createSurveyFile(room_id, percent, day,time):
    ''' Enter the website details into the database. '''
    con = sql.connect("wicount.sqlite3")
    cur = con.cursor()
    today = datetime.now()
    day = int(day)
#     today = today.strftime('%Y-%m-%d')
    thisDay=datetime.today().weekday()
    if thisDay == int(day):
        today = today.strftime('%Y-%m-%d')
    elif thisDay > day:
        diff = thisDay - day
        today = today - timedelta(days=diff)
        today = today.strftime('%Y-%m-%d')
    elif thisDay < day:
        diff = (thisDay + 7) - day
        today = today - timedelta(days=diff)
        today = today.strftime('%Y-%m-%d')
        
    dt = str(today) + " " + time
    #print( "dt", dt)
    day = GetDay(day)
    details = [room_id, dt, day, percent]
    try:
        cur.execute('INSERT OR REPLACE INTO survey VALUES (?,?,?,?)', details)
        con.commit()
        con.close()
        return ("Thank you for your participation")
    except OperationalError:
        con.close()
        return ("There was an error adding the details please try again")

