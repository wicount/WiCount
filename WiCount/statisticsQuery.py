import sqlite3 as sql
from sqlite3 import OperationalError
import json

def overallReport():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT
    (sum(case when PredictedPercentage > '0' then 1 else 0 end)*1.0/count(*)*1.0)*100.0 as frequency,
    AVG(PredictedPercentage) as occupancy,
    ((sum(case when PredictedPercentage > '0' then 1 else 0 end)*1.0/count(*)*1.0) * (AVG(PredictedPercentage)/100.0))*100.0 as Utilisation,
    room 
    FROM analytics  GROUP BY room''').fetchall()
    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def percentage_utilisation():

    con = sql.connect("wicount.sqlite3")
    #con.row_factory = sql.Row # Enables column access by name: row['column_name']

    cur = con.cursor()

    sqlstring = 'SELECT room_id, PredictedPercentage, count(*) as count, room \
                From analytics \
                GROUP BY room_id, PredictedPercentage'

    try:
        percentage = cur.execute(sqlstring).fetchall()
        roomCounter = 1
        json_data = []
        roomdata = []
        data = {}
        for row in percentage:
            #print(row)
            if roomCounter == row[0]:
                if row[1] == 0:
                    data["Low"]= row[2]
                elif row[1] == 50:
                    data["Med"]= row[2]
                else:
                    data['High'] = row[2]
                data["name"] = row[3]
            else:
                roomdata.append(data)
                roomCounter += 1
                data = {}
                if row[1] == 0:
                    data["Low"]= row[2]
                elif row[1] == 50:
                    data["Med"]= row[2]
                else:
                    data['High'] = row[2]
                
        roomdata.append(data)       
        print("roomdata: ", roomdata)
        json_data.append(roomdata)
        con.commit()
        json_data = json.dumps(roomdata)
        print("json_data: ", json_data)
        return json_data
    except OperationalError:
        con.close()
        return "An error occurred while calculating percentage utilisation"
    except Exception as e:
        print(e)

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



def greaterOccupancy(greater):

    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()
    try:
        great = int(greater)
    except:
        great = 0
        
    rows = cur.execute("SELECT date, Room, ((PredictedPercentage*Capacity)/100) as occupancy FROM analytics WHERE occupancy > ?",((great),) ).fetchall()
  
    con.commit()
    con.close()
  
    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)
#     
# 
def lesserOccupancy(lesser):

    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()
    try:
        less = int(lesser)
    except:
        less = 0
    rows = cur.execute("SELECT date, Room, ((PredictedPercentage*Capacity)/100) as occupancy FROM analytics WHERE occupancy < ?",((less),) ).fetchall()
  
    con.commit()
    con.close()
  
    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)


if __name__ == '__main__':
    
    print(greaterOccupancy(100))
    print(emptyRooms())
    print(fullRooms())
    

