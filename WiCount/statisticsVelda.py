import sqlite3 as sql
from sqlite3 import OperationalError
import json
from blaze.expr.reductions import count
from nntplib import lines

def allthree():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT \
            (sum(case when PredictedPercentage > '0' then 1 else 0 end)*1.0/count(*)*1.0)*100.0 as frequency,\
            AVG(PredictedPercentage) as occupancy,\
            ((sum(case when PredictedPercentage > '0' then 1 else 0 end)*1.0/count(*)*1.0) * (AVG(PredictedPercentage)/100.0))*100.0 as Utilisation,\
            room \
            FROM analytics  GROUP BY room''').fetchall()
            
#     expaination:
#     count the number of percentage>0 and divide by the total count
#     get the average of the percentage
#     divide the above two lines (It would allow me divide the variables)

    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

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
    print(allthree())

