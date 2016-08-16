import sqlite3 as sql
from sqlite3 import OperationalError
import json

def frequencyReport():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT AVG(PredictedPercentage) as frequency, room FROM analytics WHERE PredictedPercentage > 0 GROUP BY room''').fetchall()
    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def occupancyReport():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT AVG(PredictedPercentage) as occupancy, room FROM analytics GROUP BY room''').fetchall()
    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def utilizationReport():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT AVG(PredictedPercentage) as utilization, room FROM analytics GROUP BY room''').fetchall()
    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

# def roomOccupancy():
#     con = sql.connect("wicount.sqlite3")
#     con.row_factory = sql.Row
#     cur = con.cursor()
# 
#     rows = cur.execute('''SELECT date, ROUND(predictions) as predictions FROM analytics GROUP BY date''').fetchall()
# 
#     con.commit()
#     con.close()
# 
#     return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def emptyRooms():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT date, Room FROM analytics WHERE PredictedPercentage = 0''').fetchall()

    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def fullRooms():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT date, Room FROM analytics WHERE PredictedPercentage = 100''').fetchall()

    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)



# def greaterOccupancy(greater):
#     return 0
# #     con = sql.connect("wicount.sqlite3")
# #     con.row_factory = sql.Row
# #     cur = con.cursor()
# #     occupancy = "SELECT ((PredictedPercentage/100)*Capacity) as occupancy FROM analytics"
# #     thisRoom = cur.execute(occupancy).fetchall()[0]
# #     rows = cur.execute("SELECT date, Room, ((PredictedPercentage/100)*Capacity) as occupancy FROM analytics WHERE %d > ?" % thisRoom,(greater,)).fetchall()
# #    
# #     con.commit()
# #     con.close()
# #    
# #     return json.dumps( [dict(ix) for ix in rows],sort_keys=False)
#     
# 
# def lesserOccupancy(lesser):
#     return 0
# #     con = sql.connect("wicount.sqlite3")
# #     con.row_factory = sql.Row
# #     cur = con.cursor()
# #  
# #     rows = cur.execute("SELECT date, Room, ((PredictedPercentage/100)*Capacity) as occupancy FROM analytics WHERE ((PredictedPercentage/100)*Capacity) <" + str(lesser)).fetchall()
# #  
# #     con.commit()
# #     con.close()
# #  
# #     return json.dumps( [dict(ix) for ix in rows],sort_keys=False)


if __name__ == '__main__':
    
    print(frequencyReport())
    print(occupancyReport())
    print(utilizationReport())
    print(emptyRooms())
    print(fullRooms())
    

