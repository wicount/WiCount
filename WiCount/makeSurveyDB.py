import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
#import numpy as np
import pandas as pd
from dateutil.parser import parse
#from _nsis import err

def UpdateCollegeTable(occupancy_details):
    #-------------------------------------------------------
    #set up hard coding this will need to be passed in.
    #-------------------------------------------------------
    
    campus = "Belfield"
    building = "Computer Science"
    #print(occupancy_details)
    for x in range (0, len(occupancy_details[0])):
        #room_ID = ""
        try:
            sql_String = "SELECT room_id FROM college WHERE campus = '" + campus + \
                            "' AND building = '" + building + "' AND room = '" + occupancy_details[0][x] + "';"
            #print ("sql_String: ", sql_String)
            c.execute(sql_String)
            room_ID = c.fetchone()
            #print("room_ID: ", room_ID)
            if room_ID:
                sql_String = "UPDATE college SET occupancy=" + str(occupancy_details[1][x]) + \
                             " WHERE room_id=" + str(room_ID[0]) + ";" 
                c.execute(sql_String)
                room_ids.append(room_ID[0])
            else:
                room = [campus,building,occupancy_details[0][x],occupancy_details[1][x]]
                c.execute('INSERT INTO college (campus, building, room, occupancy) VALUES (?, ?, ?, ?)', room)
                c.execute(sql_String)
                room_ID = c.fetchone()[0]
                room_ids.append(room_ID)
        except OperationalError:
            print ("Command skipped: ", sql_String)
        con.commit()
    #print (room_ids)
    return room_ids

def UpdateSurveyTable(all_details):
    print(all_details)
    try:
        c.executemany('INSERT INTO survey VALUES (?,?,?,?)', all_details)
    except OperationalError:
        print ("Command skipped: ", all_details)
    con.commit()
    

def ConvertToCSV(file):
    data_xls = pd.read_excel(file, 'JustData', index_col=None)
    data_xls.to_csv('survey.csv', encoding='utf-8')
    
    
def GetRoomNo(room):
    #print("in GetRoomNo: ", room)
    if room != "":
        room = room.replace(".", "")
        room_no = room[:1] + "-"+ room[1:]
    else:
        room_no = ""
    #print ("room ", room_no)
    return room_no
    
def GetTime(data):
    # format the time for the database so it matches with other time formats
    data = data.split("-")
    time = data[0]
    #print ("data: ", type(time))
    if len(time) == 4:
        time = str("0") + str(time[:1]) + ":" + str(time[2:]) + str(":00")
    else:
        time = str(time[:2]) + ":" + str(time[3:]) + ":00"
    #print ("Time: ", time, " len: ", len(time))
    return time


con = lite.connect('wicount.sqlite3')
c=con.cursor()

# if the table doesn't exist create it.
try:
    c.execute ("create table if not exists survey(room_id INTEGER  NOT NULL, date DATETIME  NOT NULL, \
                day VARCHAR(3), percentage FLOAT, PRIMARY KEY (room_id, date));")
    c.execute ("create table if not exists college(room_id INTEGER PRIMARY KEY, campus VARCHAR(8), \
                building VARCHAR(16), room VARCHAR(5), occupancy INTEGER);")
except OperationalError:
    print("couldn't create the table")
con.commit()
     


#-------------------------------------------------------
#set up variables.
#-------------------------------------------------------
dayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
timeList = ["9.00-10.00", "10.00-11.00", "11.00-12.00", "12.00-13.00", \
            "13.00-14.00", "14.00-15.00", "15.00-16.00", "16.00-17.00"]
full_details = []
room_ids = []
occupancy_details = []
day = "Mon"    #initialise variable
DateTime = ""
date = ""


# Got help from http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
os.chdir("Survey")
#set up hard codeing this will need to be passed in.
for file in glob.glob("*.xlsx"):
    # Get the details from the spreadsheet
    sheet = pd.read_excel(file, 'JustData')
    sheet = sheet.dropna(how='all')
    sheet = sheet.dropna(axis='columns', how='all')
    sheet.to_csv('survey.csv', encoding='utf-8')
    dataArray = sheet.as_matrix()
    
    for data in dataArray:
        if data[0] in dayList:
            day = data[0]
            day = day[:3]
        elif data[1] == "Room No.":
            details = []
            if full_details == []:
                for x in range(2, len(data),1):
                    room_no = GetRoomNo(data[x])
                    details.append(room_no)
                occupancy_details.append(details)
        elif data[0] == "Time":
            if len(occupancy_details) == 1:
                details = []
                for x in range(2, len(data),1):
                    details.append(data[x])
                    #print("velda: ", details)
                occupancy_details.append(details)
                room_ids = UpdateCollegeTable(occupancy_details)
        elif data[0] in timeList:
            details = []
            date_str = date + " " + GetTime(data[0])
            for x in range(2, len(data),1):
                details = [room_ids[x-2], date_str, day, data[x]]
            full_details.append(details)
        elif "OCCU" in data[0]:
            continue
        else:
            date = parse(data[0])
            date = date.strftime('%Y-%m-%d')
        #end if
    UpdateSurveyTable(full_details)
    

con.close()