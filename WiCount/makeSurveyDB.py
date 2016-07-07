import db
import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
import pandas as pd
from dateutil.parser import parse
import wicount

def UpdateRoomTable(occupancy_details):
    ''' update the details of the room table'''
    #Occupancy_details is a list of (room number, capacity)
    # and returns a list of [campus, building, room number, capacity]
    #-------------------------------------------------------
    #set up hard coding this will need to be passed in.
    #-------------------------------------------------------
    room_ids = []
    campus = "Belfield"
    building = "Computer Science"
    for x in range (0, len(occupancy_details[0])):
        #need to return = [campus, building, room number, capacity]
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
    ''' format the room number so it is in the standard format B-002'''
    if room != "":
        room = room.replace(".", "")
        room_no = room[:1] + "-"+ room[1:]
    else:
        room_no = ""
    #print ("room ", room_no)
    return room_no

con = db.get_connection()
c=con.cursor()

# Create all the database tables
wicount.SetUpDatabase()

     
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
# go to the survey directory
os.chdir("Survey")

# for each file in the directory
for file in glob.glob("*.xlsx"):
    # Get the details from the spreadsheet
    sheet = pd.read_excel(file, 'JustData')
    sheet = sheet.dropna(how='all') #drop all rows that contain nothing
    sheet = sheet.dropna(axis='columns', how='all') # drop all columns that containg nothing
    sheet.to_csv('survey.csv', encoding='utf-8') #save it as a csv
    dataArray = sheet.as_matrix()   # create a matrix from the data
    
    for data in dataArray:
        if data[0] in dayList:  
            #if the first cell is the day format the day
            day = data[0]
            day = day[:3]
        elif data[1] == "Room No.":
            # if the second cell is "Room No." get the list of the room numbers
            #     Room No.    B004    B002    B003    B1.06    B1.08    B1.09
            details = []
            if fullDetails == []:
                for x in range(2, len(data),1):
                    roomNo = GetRoomNo(data[x])
                    details.append(roomNo)
                occupancyDetails.append(details) # occupancyDetails:  [['B-004', 'B-002', 'B-003', 'B-106', 'B-108', 'B-109']]
                #print("occupancyDetails: ", occupancyDetails)
        elif data[0] == "Time":
            # if the first cell is Time this row contains the capacity of the room
            # Update the room table with these details and get the room ID from the room table
            if len(occupancyDetails) == 1:
                details = []
                for x in range(2, len(data),1):
                    details.append(data[x])
                occupancyDetails.append(details)
                roomIDs = UpdateRoomTable(occupancyDetails)
        elif data[0] in timeList:
            # If the first cell is a time then set up the date
            # 9.00-10.00        0.25    0.25    0.25    1    0    0
            details = []
            dateStr = date + " " + wicount.GetTime(data[0])
            # for each percentage build up the list of sql string. [1, '2015-11-13 16:00:00', 'Fri', 0.25]
            for x in range(2, len(data),1):
                details = [roomIDs[x-2], dateStr, day, data[x]]
                fullDetails.append(details)
        elif "OCCU" in data[0]:
            # if the first cell is CSI Classroom OCCUPANCY skip and continue to next loop
            # Chose OCCUPANCY for when the building changes
            continue
        else:
            # otherwise it is the date field so parse the date into the format 2015-Nov-11
            date = parse(data[0])
            date = date.strftime('%Y-%m-%d')
        #end if
        #update the survey table with the list created above
        UpdateSurveyTable(fullDetails)
    # end for
con.close()