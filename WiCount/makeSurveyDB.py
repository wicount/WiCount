import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
import numpy as np
import pandas as pd
import datetime
from dateutil.parser import parse
import math
from _nsis import err


def ConvertToCSV(file):
    import pandas as pd
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

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError as err:
        return False
    
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

# con = lite.connect('wicount.sqlite3')
# c=con.cursor()
# # if the table doesn't exist create it.
# try:
#     c.execute("SELECT * from survey")
# except OperationalError:
#     c.execute ("CREATE TABLE survey(campus varchar(8),building varchar(16),room varchar(5), day varchar(3), \
#             time time, date date, percentage int, totaloccupancy int);")
# con.commit()
     
#-------------------------------------------------------
#set up hard coding this will need to be passed in.
#-------------------------------------------------------

campus = "Belfield"
building = "Computer Science"
dayList = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
timeList = ["9.00-10.00", "10.00-11.00", "11.00-12.00", "12.00-13.00", \
            "13.00-14.00", "14.00-15.00", "15.00-16.00", "16.00-17.00"]
full_details = []
occupancy_details = []
day = "Mon"    #initialise variable

# Got help from http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
os.chdir("Survey")
#set up hard codeing this will need to be passed in.
for file in glob.glob("*.xlsx"):
    sheet = pd.read_excel(file, 'JustData')
    sheet = sheet.dropna(how='all')
    sheet = sheet.dropna(axis='columns', how='all')
    #print(len(sheet))
    sheet.to_csv('survey.csv', encoding='utf-8')
    #print(type(sheet))
    dataArray = sheet.as_matrix()
    print(dataArray)
    for data in dataArray:
        #print(data[0])
        if data[0] in dayList:
            day = data[0]
            day = day[:3]
            #print (day)
        elif data[1] == "Room No.":
            #print("build the room string")
            details = []
            if full_details == []:
                for x in range(2, len(data),1):
                    room_no = GetRoomNo(data[x])
                    details.append(room_no)
                    #print("velda: ", details)
                full_details.append(details)
                occupancy_details.append(details)
        elif data[0] == "Time":
            if len(occupancy_details) == 1:
                details = []
                for x in range(2, len(data),1):
                    details.append(data[x])
                    #print("velda: ", details)
                occupancy_details.append(details)
        elif data[0] in timeList:
            details = []
            for x in range(2, len(data),1):
                details.append(data[x])
            #print("velda: ", details)
            full_details.append(details)
        elif "OCCU" in data[0]:
            continue
        else:
            date = parse(data[0])
            #print(date)
            date = date.strftime('%Y-%b-%d')
            #print(date)
            
        #end if
        
print("occupancy_details: ")
for x in range(0,len(occupancy_details)-1):
    print(occupancy_details[x])
print("")
print("full_details: ")
for x in range(0, len(full_details) -1):
    print(full_details[x])
print("")
print ("day: ", day)
print("campus: ", campus)
print("building: ", building)    
#     wb = openpyxl.load_workbook(file)
#     sheet = wb.get_sheet_by_name("JustData")
#          
#     sqlvalues = []
#     print(sheet)
#     print('velda ',sheet.max_column)
#     print("velda2 ", get_column_letter(sheet.max_column))
#     row_count = sheet.max_row - 1
#     print ('row_count ', row_count)
    #column_count = letter_to_index(sheet.max_col()) + 1
    #print('column_count ', column_count)
    #fullSheet = row_count + column_count
#     print(fullSheet)
#     table = np.array([[cell.value for cell in col] for col in sheet['A1':fullSheet]])
#     print(table)
#         for line in table:
#             print(line)
#             start_time = GetTime(line[0])
#             #build sql string
#             for i in range(1,len(line),2):
#                 db_values = [campus, building, room_no, GetDay(i), start_time, line[i], line[i+1]]
#                 sqlvalues.append(db_values)
#             try:
#                 c.executemany('INSERT INTO timetable VALUES (?,?,?,?,?,?,?)', sqlvalues)
#                 
#             except OperationalError:
#                 print ("Command skipped: ", sqlvalues)
#             print("done: ", sqlvalues)  
#             con.commit()
# cur.execute("DROP TABLE IF EXISTS Cars")
#     cur.execute("CREATE TABLE Cars(Id INT, Name TEXT, Price INT)")
#     cur.executemany("INSERT INTO Cars VALUES(?, ?, ?)", cars)
#con.close() 