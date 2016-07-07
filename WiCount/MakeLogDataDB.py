import db
import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os
from dateutil.parser import parse
import wicount


def ExtractDataCSV(fileName):
    fileHandle = open(fileName)
    full_db_values=[]
    for line in fileHandle:
        if line[:9] == "Generated":
            date = line.split()[1]
            date = parse(date[:-1])
            date = date.strftime('%Y-%m-%d')
        elif line[:8] == "Belfield" or line[:7] == "Smurfit":
            #Hard coding " > " I don't think this is ideal.
            data = line.replace(' > ',',').split(",")
            
            day = data[3].partition(' ')[0]
            #We only want relevant data so get rid of data outside of this.
            if day == "Sat" or day == "Sun":
                return ""   #skip weekends
            time = data[3].split(' ')[3]
            if time < "09:00:00" or time > "17:00;00":
                continue
        
            date_time = date + " " + time
            #[campus, building, room number, capacity]
            room_details = [data[0], data[1], data[2],0]
            room_ID = wicount.GetRoomID(room_details)
        
            db_values = [room_ID, date_time, day, data[4]]
            full_db_values.append(db_values)
    if full_db_values == []:
        return ""
    else:        
        return full_db_values

con = db.get_connection()
c=con.cursor()

# Create all the database tables
wicount.SetUpDatabase()
            
# Got help from http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
os.chdir("CSILogs")
for file in glob.glob("*.csv"):
    sqlvalues = ExtractDataCSV(file)
    # Execute every command from the input file
    if sqlvalues != "":
        try:
            c.executemany('INSERT OR REPLACE INTO logdata VALUES (?,?,?,?)', sqlvalues)
        except OperationalError:
            print ("Command skipped: ", sqlvalues)
        con.commit()
con.close() 
print("finished")