import sqlite3 as lite
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

con = lite.connect('wicount.sqlite3')

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM survey")

    rows = cur.fetchall()

    for row in rows:
        print(row)

full_data = []
data_list = []

for row in rows:
    cur.execute("SELECT * FROM college WHERE room_id = '" + str(row[0]) + "'")
    college = cur.fetchall()[0]
    
    #get time and date fields.
    fromDate = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
    toDate = fromDate + timedelta(hours=1)
    time = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S").time()
    
    #only continue if we have timetable data.
    cur.execute("SELECT * FROM timetable WHERE room_id = '" + str(row[0]) + \
                "' and day = '" + row[2] + "' AND  time = '" + str(time) + "'")
    timetable = cur.fetchall()
    if timetable == []:
        continue
    timetable = timetable[0]
    
    #print("SELECT MAX(count) FROM logdata WHERE room_id = '" + str(row[0]) + \
    #            "' and date BETWEEN '" + str(fromDate) + "' AND '" + str(toDate) + "'")
    cur.execute("SELECT MAX(count) FROM logdata WHERE room_id = '" + str(row[0]) + \
                "' and date BETWEEN '" + str(fromDate) + "' AND '" + str(toDate) + "'")
    logData = cur.fetchall()[0]
    
    cur.execute("SELECT percentage FROM survey WHERE room_id = '" + str(row[0]) + \
                "' and date = '" + str(fromDate) + "'")
    survey = cur.fetchall()[0]
    #print("row: ", row)
    #print("college: ", college)
    #print("timetable: ", timetable)
    #print("logData: ", logData)
    #print ("survey: ", survey)
    #print('Campus: ',college[1])
    #print('Building: ',college[2])
    #print('Room: ',college[3])
    #print('Occupancy: ',college[4])
    #print('Date: ',row[1])
    #print('Day: ',row[2], ' SurveyPercentage: ',survey[0],)
    #print('MaxCount: ',logData[0], ' Module: ',timetable[3], ' NoStudents: ',timetable[4])
    
    data_list = [college[1], college[2], college[3], college[4], \
                 row[1], row[2], survey[0], \
                 logData[0], timetable[3], timetable[4]]
    full_data.append(data_list)
    
data = pd.DataFrame(full_data, columns=('Campus', 'Building', 'Room', 'Occupancy', \
                          'Date', 'Day', 'SurveyPercentage', \
                            'MaxCount', 'Module', 'NoStudents'))
data.head(2)
print(data)
