#Set path for libaries on server
#import sys
#sys.path.insert(0, "/home/student/anaconda3/lib/python3.4/site-packages")

import MakeLogDataDB
import makeSurveyDB
import makeTimeTableDB
import glob, os
import wicount
import db
import DataAnalysis

#Connect to the database
con = db.get_connection()
c=con.cursor()
# Create all the database tables
wicount.SetUpDatabase()
MakeLogDataDB.main()
makeSurveyDB.main()
makeTimeTableDB.main()

#Run the analytics algorithm
DataAnalysis.main()

#Close the database connection
con.close() 
