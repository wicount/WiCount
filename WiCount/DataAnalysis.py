import sqlite3 as lite
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
#from docutils.nodes import list_item
from dateutil.parser import parse

def GetAllWeekNos(start, end):
    c.execute("SELECT DISTINCT week_no from timetable where week_no >= '" \
              + start+ "' AND week_no <= '"+ end+ "'")
    data = c.fetchall()
    week_nos = []
    for weeks in data:
        #print(weeks)
        list_item = weeks[0].split("/")
        list_item = [ int(x) for x in list_item ]
        list_item.append(weeks[0])
        week_nos.append(list_item)
        #print(week_nos)
    return week_nos

def WeekNo(date):
    weekno = date.isocalendar()
    return weekno

def FormatWeekNo(week):
    return str(week[1]) + "/" + str(week[0])

def GetWeek(date):
    ''' get the relevant week from the timetable table'''
    
    week = date.isocalendar()
    week_nos = FormatWeekNo(week)
    
    if week[1] >= WeekNo(parse("1 Sept" + str(week[0])))[1]:
        semester_beg = WeekNo(parse("1 Sept" + str(week[0])))
        semester_end = WeekNo(parse("31 Dec" + str(week[0]))) 
    else:
        semester_beg = WeekNo(parse("1 Jan" + str(week[0])))
        semester_end = WeekNo(parse("30 May" + str(week[0])))
    
    semester_beg = FormatWeekNo(semester_beg)
    semester_end = FormatWeekNo(semester_end)
    week_nos = GetAllWeekNos(semester_beg, semester_end)
    
    if week_nos[0][1] % 2:
        even = week_nos[0][2]
        odd = week_nos[1][2]
    else:
        even = week_nos[1][2]
        odd = week_nos[0][2]
    
    if week[1] % 2:
        return even
    else:
        return odd


con = lite.connect('wicount.sqlite3')
c=con.cursor()
with con:    
    c = con.cursor()    
    c.execute("SELECT * FROM survey")

    rows = c.fetchall()

    for row in rows:
        print(row)

full_data = []
data_list = []

for row in rows:
    c.execute("SELECT * FROM room WHERE room_id = '" + str(row[0]) + "'")
    college = c.fetchall()[0]
    
    #get time and date fields.
    fromDate = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S")
    toDate = fromDate + timedelta(hours=1)
    time = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S").time()
    week_no = GetWeek(fromDate)
    
    #only continue if we have timetable data.
    c.execute("SELECT * FROM timetable WHERE room_id = '" + str(row[0]) + \
                "' and day = '" + row[2] + "' AND  time = '" + str(time) + "' AND week_no = '" + week_no + "'")
    timetable = c.fetchall()
    if timetable == []:
        continue
    timetable = timetable[0]
    
#     print("SELECT MAX(count) FROM logdata WHERE room_id = '" + str(row[0]) + \
#                  "' and date BETWEEN '" + str(fromDate) + "' AND '" + str(toDate) + "'")
#     c.execute("SELECT MAX(count) FROM logdata WHERE room_id = '" + str(row[0]) + \
#                 "' and date BETWEEN '" + str(fromDate) + "' AND '" + str(toDate) + "'")
#     logData = c.fetchall()[0]
#Velda tryting to get all rows.
    c.execute("SELECT count, date FROM logdata WHERE room_id = '" + str(row[0]) + \
                 "' and date BETWEEN '" + str(fromDate) + "' AND '" + str(toDate) + "'")
    logData = c.fetchall()
    # Only use if we have all the data for all the days
    if logData == []:
        continue
    
    c.execute("SELECT percentage FROM survey WHERE room_id = '" + str(row[0]) + \
                "' and date = '" + str(fromDate) + "'")
    survey = c.fetchall()[0]
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
    
    #for logData
    for i in range(0, len(logData)):
        data_list = [college[1], college[2], college[3], college[4], \
                 row[1], row[2], survey[0], \
                 logData[i][0], logData[i][1], timetable[4], timetable[5], timetable[3]]
        full_data.append(data_list)
    
data = pd.DataFrame(full_data, columns=('Campus', 'Building', 'Room', 'Capacity', \
                          'Date', 'Day', 'SurveyPercentage', \
                            'Count', 'LogDate', 'Module', 'NoStudents', 'WeekNo'))
data.head(2)
print(data)
#output to a file
data.to_csv("full_dataset.csv")
