import db
import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
import pandas as pd
from dateutil.parser import parse
import wicount

def UpdateRoomTable(occupancy_details):
    ''' update the details of the room table'''
    #-------------------------------------------------------
    #set up hard coding this will need to be passed in.
    #-------------------------------------------------------
    
    campus = "Belfield"
    building = "Computer Science"
    for x in range (0, len(occupancy_details[0])):
        #[campus, building, room number, capacity]
        room_details = [campus, building, occupancy_details[0][x], occupancy_details[1][x]]
        room_ids.append(wicount.GetRoomID(room_details))
    return room_ids

def UpdateSurveyTable(all_details):
    ''' update the survey table'''
    #print(all_details)
    try:
        c.executemany('INSERT OR REPLACE INTO survey VALUES (?,?,?,?)', all_details)
    except OperationalError:
        print ("Command skipped: ", all_details)
    con.commit()
    

def ConvertToCSV(file):
    ''' convert the excel sheet to a csv'''
    data_xls = pd.read_excel(file, 'JustData', index_col=None)
    data_xls.to_csv('survey.csv', encoding='utf-8')
    
    
def GetRoomNo(room):
    ''' format the room number so it is in the standard format'''
    if room != "":
        room = room.replace(".", "")
        room_no = room[:1] + "-"+ room[1:]
    else:
        room_no = ""
    #print ("room ", room_no)
    return room_no

con = db.get_connection()
c=con.cursor()

# if the table doesn't exist create it.
try:
    c.execute ("create table if not exists survey(room_id INTEGER  NOT NULL, date DATETIME  NOT NULL, \
                day VARCHAR(3), percentage FLOAT, PRIMARY KEY (room_id, date));")
except OperationalError:
    print("couldn't create the table")
con.commit()
     
#-------------------------------------------------------
#set up variables.
#-------------------------------------------------------
dayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
timeList = ["9.00-10.00", "10.00-11.00", "11.00-12.00", "12.00-13.00", \
            "13.00-14.00", "14.00-15.00", "15.00-16.00", "16.00-17.00"]
fullDetails = []
roomIDs = []
occupancyDetails = []
day = "Mon"    #initialise variable
dateTime = ""
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
            if fullDetails == []:
                for x in range(2, len(data),1):
                    roomNo = GetRoomNo(data[x])
                    details.append(roomNo)
                occupancyDetails.append(details)
                #print(occupancyDetails)
        elif data[0] == "Time":
            if len(occupancyDetails) == 1:
                details = []
                for x in range(2, len(data),1):
                    details.append(data[x])
                occupancyDetails.append(details)
                room_ids = UpdateRoomTable(occupancyDetails)
        elif data[0] in timeList:
            details = []
            dateStr = date + " " + wicount.GetTime(data[0])
            #print(room_ids)
            for x in range(2, len(data),1):
                details = [roomIDs[x-2], dateStr, day, data[x]]
                fullDetails.append(details)
        elif "OCCU" in data[0]:
            continue
        else:
            date = parse(data[0])
            date = date.strftime('%Y-%m-%d')
        #end if
        UpdateSurveyTable(fullDetails)
    # end for
con.close()