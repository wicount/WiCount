import MakeLogDataDB
import makeSurveyDB
import makeTimeTableDB
import glob, os
import wicount
import db

con = db.get_connection()
c=con.cursor()

# Create all the database tables
wicount.SetUpDatabase()

MakeLogDataDB.main()
makeSurveyDB.main()
makeTimeTableDB.main()

con.close() 