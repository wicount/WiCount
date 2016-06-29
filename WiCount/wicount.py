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

def GetRoomID(details):
    ''' Get the room ID from the database. 
    
    Details need to passed in in the format [campus, building, room number, capacity].
    where occupancy is the capacity of the room. Will return the room ID as an integer'''
    con = db.get_connection()
    #con = lite.connect('wicount.sqlite3')
    c=con.cursor()
    try:
        c.execute ("create table if not exists room(room_id INTEGER PRIMARY KEY, campus VARCHAR(8), \
                    building VARCHAR(16), room VARCHAR(5), capacity INTEGER);")
        con.commit()
    except OperationalError:
        print("Couldn't create the room table")
    
    try:
        sql_String = "SELECT room_id FROM room WHERE campus = '" + details[0] + \
                    "' AND building = '" + details[1] + "' AND room = '" + details[2] + "';"
        #print ("sql_String: ", sql_String)
        c.execute(sql_String)
        room_ID = c.fetchone()
        print ("here: ", room_ID)
        if room_ID:
            room_ID =  room_ID[0]
            if details[3] > 0:
                #update the occupancy if these details are passed in.
                sql_String = "UPDATE room SET capacity=" + str(details[3]) + \
                             " WHERE room_id=" + str(room_ID) + ";"
                c.execute(sql_String)
                con.commit()
            print ("velda: ", room_ID)
        else:
            room = [details[0],details[1],details[2],details[3]]
            c.execute('INSERT INTO room (campus, building, room, capacity) VALUES (?, ?, ?, ?)', room)
            c.execute(sql_String)
            con.commit()
            room_ID = c.fetchone()[0]
        print("velda")
        con.commit()
        print("velda2")
    except OperationalError:
        print ("Command skipped: ", sql_String)

    return room_ID

#GetRoomID("here")
