import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
import openpyxl
import numpy as np

def GetRoomNo(room):
    room_no = room[:1] + "-"+ room[1:2] + room [3:]
    #print ("room ", room_no)
    return room_no

def GetTime(data):
    # format the time for the database so it matches with other time formats
    data = data.split()
    #print ("data: ", data)
    time = data[0]
    if len(time) == 4:
        time = str("0") + str(time) + str(":00")
    else:
        time = str(time) + ":00"
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

con = lite.connect('wicount.sqlite3')
c=con.cursor()
# if the table doesn't exist create it.
try:
    c.execute("SELECT * from timetable")
except OperationalError:
    c.execute ("CREATE TABLE timetable(campus varchar(8),building varchar(16),room varchar(5), day varchar(3), \
            time time, module varchar(12), no_students int);")
con.commit()
     
#-------------------------------------------------------
#set up hard coding this will need to be passed in.
#-------------------------------------------------------

campus = "Belfield"
building = "Computer Science"
       
# Got help from http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
os.chdir("Survey")
#set up hard codeing this will need to be passed in.
campus = "Belfield"
building = "Computer Science"
for file in glob.glob("*.xlsx"):
    wb = openpyxl.load_workbook(file)
    sheet = wb.get_sheet_by_name("JustData")
    sqlvalues = []
    #print(sheet)
    room_no = GetRoomNo(sheet)
    if sheet != "All":
        sheetData = wb.get_sheet_by_name(sheet)
        table = np.array([[cell.value for cell in col] for col in sheetData['A3':'K11']])
        #print(table)
        for line in table:
            print(line)
            start_time = GetTime(line[0])
            #build sql string
            for i in range(1,len(line),2):
                db_values = [campus, building, room_no, GetDay(i), start_time, line[i], line[i+1]]
                sqlvalues.append(db_values)
            try:
                c.executemany('INSERT INTO timetable VALUES (?,?,?,?,?,?,?)', sqlvalues)
                
            except OperationalError:
                print ("Command skipped: ", sqlvalues)
            print("done: ", sqlvalues)  
            con.commit()
con.close() 