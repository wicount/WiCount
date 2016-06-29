import db
import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
import openpyxl
import numpy as np
import wicount

def GetRoomNo(room):
    room_no = room[:1] + "-"+ room[1:2] + room [3:]
    #print ("room ", room_no)
    return room_no

def GetTime(data):
    ''' Get the time in the correct format.  
    
    This is for timetable type times is 9:00 - 10:00.  It will return 09:00:00'''
    data = data.split("-")
    time = data[0].strip()
    #print ("data: ", type(time))
    if len(time) == 4:
        time = str("0") + str(time[:1]) + ":" + str(time[2:]) + str(":00")
    else:
        time = str(time[:2]) + ":" + str(time[3:]) + ":00"
    #print ("Time: ", time, " len: ", len(time))
    return time

def GetDay(i):
    return {
        1: "Mon",
        3: "Tue",
        5: "Wed",
        7: "Thu",
        9: "Fri",
    }.get(i, 1)
    
con = db.get_connection()
#con = lite.connect('wicount.sqlite3')
c=con.cursor()
# if the table doesn't exist create it.
try:
    c.execute ("create table if not exists timetable(room_id INTEGER NOT NULL, day varchar(3), \
            time time, module varchar(12), no_students int, PRIMARY KEY (room_id, day, time));")
except OperationalError:
    print("Timetable table couldn't be created")
con.commit()
      
# Got help from http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
os.chdir("timetable")

#set up hard codeing this will need to be passed in.
campus = "Belfield"
building = "Computer Science"
for file in glob.glob("*.xlsx"):
    wb = openpyxl.load_workbook(file)
    sheetnames = wb.get_sheet_names()
    sqlvalues = []
    for sheet in sheetnames:
        #print(sheet)
        if sheet != "All":
            room_details = [campus, building, GetRoomNo(sheet),0] #0 on end as we don't know capacity.
            room_id = wicount.GetRoomID(room_details)
            sheetData = wb.get_sheet_by_name(sheet)
            table = np.array([[cell.value for cell in col] for col in sheetData['A3':'K11']])
            #print(table)
            for line in table:
                #print(line)
                sqlvalues = []
                start_time = GetTime(line[0])
                #build sql string
                for i in range(1,len(line),2):
                    db_values = [room_id, GetDay(i), start_time, line[i], line[i+1]]
                    sqlvalues.append(db_values)
                try:
                    #print(sqlvalues)
                    c.executemany('INSERT OR IGNORE INTO timetable VALUES (?,?,?,?,?)', sqlvalues)
                    #print("done: ", sqlvalues) 
                except OperationalError:
                    print ("Command skipped: ", sqlvalues)
                con.commit()
con.close() 