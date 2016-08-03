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

def GetBuildingDetails(room_id):
    ''' Get the details for all the rooms in the building. '''
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row # This enables column access by name: row['column_name'] 
    cur = con.cursor()
    sqlString = "SELECT * FROM room WHERE room_id = '" + str(room_id) + "';"
#     print("velda,", sqlString)
    try:
        thisRoom = cur.execute(sqlString).fetchall()[0]
        con.commit()
    except OperationalError:
        return ("There was an error adding the details please try again")
    sqlString = "SELECT * FROM room WHERE campus = '" + thisRoom[1] + "' AND building = '" + thisRoom[2] + "';"
    allRooms = cur.execute(sqlString).fetchall()
    con.commit()
    return json.dumps( [dict(ix) for ix in allRooms] ) #CREATE JSON

def WeekNo(date):
    weekno = date.isocalendar()
    return weekno[1]

def StatsForRoom(room_id):
    con = sql.connect('wicount.sqlite3')
    with con:    
        c = con.cursor()    
#         velda adding to get latest two weeks of data
        c.execute("SELECT MAX(date) FROM survey WHERE room_id = '" + str(room_id) + "';")
        endDate = c.fetchall()[0]
        endDate = datetime.strptime(endDate[0], "%Y-%m-%d %H:%M:%S")
        startDate = endDate + timedelta(days=-14)
        print ("endDate",endDate)
        print("startdate", startDate)
        c.execute("SELECT * FROM survey WHERE room_id = '" + str(room_id) + "' \
                            AND date BETWEEN '"+ str(startDate)+"' AND '"+str(endDate)+"';")
#         c.execute("SELECT * FROM survey WHERE room_id = '" + str(room_id) + "';")
#         end change to get latest two weeks    
        rows = c.fetchall()
        week1_data = []
        week2_data = []
        json_data = []
        even = WeekNo(parse(rows[0][1]))
#         print(even)
        for row in rows:
            data = {}
            date = row[1]
            data['day'] = row[2]
            data['hour'] = date[11:16]
            data['percent'] = row[3]
#             print(WeekNo(parse(date)), ", ", even, ", ")
#             print(WeekNo(parse(date)) == even)
            if WeekNo(parse(date)) == even:
                data['week'] = "Even"
                data['date'] = str(parse(date).strftime('%d, %b %Y'))
                c.execute("SELECT room FROM room WHERE room_id = '" + str(room_id) + "';")
                room = c.fetchall()[0]
                data['room'] = room
                week2_data.append(data)
            else:
                data['week'] = "Odd"
                data['date'] = str(parse(date).strftime('%d, %b %Y'))
                c.execute("SELECT room FROM room WHERE room_id = '" + str(room_id) + "';")
                room = c.fetchall()[0]
                data['room'] = room
                week1_data.append(data)
#             print(data)
        json_data = [week1_data, week2_data]
        print(json_data)
        return(json.dumps(json_data))
    
#print(GetBuildingDetails(2))