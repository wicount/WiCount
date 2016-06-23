import sqlite3 as lite
from sqlite3 import OperationalError
import glob, os

def ExtractDataCSV(fileName):
    fileHandle = open(fileName)
    full_db_values=[]
    for line in fileHandle:
        if line[:9] == "Generated":
            date = line.split()[1]
            date = date[:-1]
            #print (date)
        elif line[:8] == "Belfield" or line[:7] == "Smurfit":
            #Hard coding " > " I don't think this is ideal.
            here = line.replace(' > ',',').split(",")
            
            day = here[3].partition(' ')[0]
            #We only want relevant data so get rid of data outside of this.
            if day == "Sat" or day == "Sun":
                return ""   #skip weekends
            time = here[3].split(' ')[3]
            if time < "09:00:00" or time > "17:00;00":
                continue
            #build insert string.
            db_values = [here[0], here[1], here[2], day, date, time, here[4]]
            full_db_values.append(db_values)
    if full_db_values == []:
        return ""
    else:        
        return full_db_values

con = lite.connect('wicount.sqlite3')
c=con.cursor()
# if the table doesn't exist create it.
try:
    c.execute("SELECT * from logdata")
except OperationalError:
    c.execute ("CREATE TABLE logdata(campus varchar(8),building varchar(16),room varchar(5),day varchar(3), \
            date date,time time,count int);")
con.commit()
            
# Got help from http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-in-python
os.chdir("CSILogs")
for file in glob.glob("*.csv"):
    sqlvalues = ExtractDataCSV(file)
    # Execute every command from the input file
    if sqlvalues != "":
        try:
            c.executemany('INSERT INTO logdata VALUES (?,?,?,?,?,?,?)', sqlvalues)
        except OperationalError:
            print ("Command skipped: ", sqlvalues)
        print("done: ", sqlvalues)  
        con.commit()
con.close() 
print("finished")