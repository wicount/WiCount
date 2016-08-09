import sqlite3 as lite
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import db
from dateutil.parser import parse

def GetAllWeekNos(start, end):
    # get the week numbers from the database
    c.execute("SELECT DISTINCT week_no from timetable where week_no >= '" \
              + start+ "' AND week_no <= '"+ end+ "'")
    data = c.fetchall()
    week_nos = []
    for weeks in data:
        list_item = weeks[0].split("/")
        list_item = [ int(x) for x in list_item ]
        list_item.append(weeks[0])
        week_nos.append(list_item)
    return week_nos

def WeekNo(date):
    #return the week number
    weekno = date.isocalendar()
    return weekno

def FormatWeekNo(week):
    # format the week number
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
    if week_nos != []:
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
    else:
        # if we only have the survey data and no timetable data
        return "none"
    
con = db.get_connection()
c=con.cursor()


def CreateTrainingSet():
    # create the dataset for the rows that have survey data
    c.execute("SELECT * FROM survey")
    rows = c.fetchall()
    
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
        if week_no == "none":
            continue
        #only continue if we have timetable data.
        c.execute("SELECT * FROM timetable WHERE room_id = '" + str(row[0]) + \
                    "' and day = '" + row[2] + "' AND  time = '" + str(time) + "' AND week_no = '" + week_no + "'")
        timetable = c.fetchall()
        if timetable == []:
            continue
        timetable = timetable[0]
    
        c.execute("SELECT count, date FROM logdata WHERE room_id = '" + str(row[0]) + \
                     "' and date BETWEEN '" + str(fromDate) + "' AND '" + str(toDate) + "'")
        logData = c.fetchall()
    
        # Only use if we have all the data for all the days
        if logData == []:
            continue
    
        c.execute("SELECT percentage FROM survey WHERE room_id = '" + str(row[0]) + \
                    "' and date = '" + str(fromDate) + "'")
        survey = c.fetchall()[0]
    
        for i in range(0, len(logData)):
            data_list = [rows[0], college[1], college[2], college[3], college[4], \
                     row[1], row[2], survey[0], \
                     logData[i][0], logData[i][1], timetable[4], timetable[5], timetable[3]]
            full_data.append(data_list)
    
    data = pd.DataFrame(full_data, columns=('room_id', 'Campus', 'Building', 'Room', 'Capacity', \
                              'Date', 'Day', 'SurveyPercentage', \
                                'Count', 'LogDate', 'Module', 'NoStudents', 'WeekNo'))
    print("Training data frame created")
    return(data)


def CreatePredictionSet():   
    # create the dataset for the all rows that have log data   
    c.execute("SELECT * FROM logdata")
    rows = c.fetchall()
    
    full_data = []
    data_list = []
    
    for row in rows:
        room_id = str(row[0])
        logDate = row[1]
        day = row[2]
        count = row[3]
        
        c.execute("SELECT * FROM room WHERE room_id = '" + room_id + "'")
        college = c.fetchall()[0]
        
        #get time and date fields.
        hourDate = datetime.strptime(logDate, "%Y-%m-%d %H:%M:%S")
        week_no = GetWeek(hourDate)
        hour = hourDate.hour
        if hour < 10:
            hour = "0" + str(hour) + ":00:00"
        else:
            hour = str(hour) + ":00:00"
        hourDate = logDate[0:11]
        hourDate = hourDate + hour
    
        #only continue if we have timetable data.
        c.execute("SELECT * FROM timetable WHERE room_id = '" + room_id + \
                    "' and day = '" + day + "' AND  time = '" + str(hour) + "' AND week_no = '" + week_no + "'")
        timetable = c.fetchall()
        if timetable == []:
            Module = ""
            NoStudents = "" 
            WeekNo =  ""
        else:
            timetable = timetable[0]
            Module = timetable[4]
            NoStudents = timetable[5]
            WeekNo = timetable[3]
        
        c.execute("SELECT percentage FROM survey WHERE room_id = '" + room_id + \
                    "' and date = '" + str(hourDate) + "'")
        survey = c.fetchall()
        if survey == []:
            survey = ""
        else:
            survey = survey[0][0]
            
        data_list = [room_id, college[3], college[4], \
                     hourDate, day, survey, count, logDate, Module, NoStudents, WeekNo]
        full_data.append(data_list)
    
    data = pd.DataFrame(full_data, columns=('room_id', 'Room', 'Capacity', \
                    'Date', 'Day', 'SurveyPercentage', 'Count', 'LogDate', 'Module', 'NoStudents', 'WeekNo'))
    print("Prediction data frame created")
    return(data)


