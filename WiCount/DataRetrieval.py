import sqlite3 as sql
import json #used to build json strings

def getAllCampusDetails():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row # This enables column access by name: row['column_name'] 
    cur = con.cursor()

    rows = cur.execute('''
    SELECT * FROM room
    ''').fetchall()

    con.commit()
    con.close()
    print ("1: ", json.dumps( [dict(ix) for ix in rows] ))
    return json.dumps( [dict(ix) for ix in rows] ) #CREATE JSON