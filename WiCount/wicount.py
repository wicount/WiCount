'''
Created on 29 Jun 2016

@author: Velda Conaty
'''
import db
import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
import openpyxl
import numpy as np


def SetUpDatabase():
    ''' Create the database tables if they don't exist'''
    con = db.get_connection()
    c=con.cursor()
    
    try:
        c.execute ("create table if not exists modules(module varchar(12), week_no varchar(7), \
                no_students int, PRIMARY KEY (module, week_no));") 
    except OperationalError:
        print("Modules table couldn't be created")
    con.commit()
    
    try:
        c.execute ("create table if not exists room(room_id INTEGER PRIMARY KEY, campus VARCHAR(8), \
                    building VARCHAR(16), room VARCHAR(5), capacity INTEGER);")     
    except OperationalError:
        print("room table couldn't be created")
    con.commit()    
    
    try:
        c.execute ("create table if not exists timetable(room_id INTEGER NOT NULL, day varchar(3), \
                time time, week_no varchar(7), module varchar(12), no_students int, \
                PRIMARY KEY (room_id, day, time, week_no) \
                FOREIGN KEY(module) REFERENCES modules(module) \
                FOREIGN KEY(room_id) REFERENCES room(room_id));")
    except OperationalError:
        print("Timetable table couldn't be created")
    con.commit()

    try:
        c.execute ("create table if not exists logdata(room_id INTEGER  NOT NULL, date DATETIME  NOT NULL, \
                    day VARCHAR(3), count INTEGER, PRIMARY KEY (room_id, date) \
                    FOREIGN KEY(room_id) REFERENCES room(room_id));")
    except OperationalError:
        print("Logdata table couldn't be created")
    con.commit()

    try:
        c.execute ("create table if not exists survey(room_id INTEGER  NOT NULL, date DATETIME  NOT NULL, \
                    day VARCHAR(3), percentage FLOAT, PRIMARY KEY (room_id, date) \
                    FOREIGN KEY(room_id) REFERENCES room(room_id));")
    except OperationalError:
        print("Survey table couldn't be created")
    con.commit()

    try:
        c.execute("CREATE TABLE IF NOT EXISTS analytics(room_id INTEGER NOT NULL, date DATETIME NOT NULL, day VARCHAR(3), GroundTruth FLOAT, \
                  SurveyPercentage INTEGER, Capacity INTEGER, Room VARCHAR(8), LogDate VARCHAR(10), MaxCount INTEGER, \
                  AverageCount FLOAT, MedianCount FLOAT, ModeCount INTEGER, Predictions FLOAT, PredictedPercentage \
                  Integer, \
                  PRIMARY KEY (room_id, LogDate)\
                  FOREIGN KEY(room_id) REFERENCES room(room_id));")

    except OperationalError:
        print("Analytics table couldn't be created")
    con.commit()
    
def GetRoomID(details):
    ''' Get the room ID from the database. 
    
    Details need to passed in in the format [campus, building, room number, capacity].
    where occupancy is the capacity of the room. Will return the room ID as an integer'''
    con = db.get_connection()
    c=con.cursor()
    try:
        sql_String = "SELECT room_id FROM room WHERE campus = '" + details[0] + \
                    "' AND building = '" + details[1] + "' AND room = '" + details[2] + "';"
        c.execute(sql_String)
        room_ID = c.fetchone()
        if room_ID:
            room_ID =  room_ID[0]
            if details[3] > 0:
                #update the occupancy if these details are passed in.
                sql_String = "UPDATE room SET capacity=" + str(details[3]) + \
                             " WHERE room_id=" + str(room_ID) + ";"
                c.execute(sql_String)
        else:
            room = [details[0],details[1],details[2],details[3]]
            c.execute('INSERT INTO room (campus, building, room, capacity) VALUES (?, ?, ?, ?)', room)
            c.execute(sql_String)
            room_ID = c.fetchone()[0]
        con.commit()
    except OperationalError:
        print ("Command skipped: ", sql_String)

    return room_ID

def GetTime(data):
    ''' Get the time in the correct format.  
    
    This is for timetable type times is 9:00 - 10:00.  It will return 09:00:00'''
    data = data.split("-")
    time = data[0].strip()
    if len(time) == 4:
        time = str("0") + str(time[:1]) + ":" + str(time[2:]) + str(":00")
    else:
        time = str(time[:2]) + ":" + str(time[3:]) + ":00"
    return time

if __name__ == '__main__':
    SetUpDatabase()
