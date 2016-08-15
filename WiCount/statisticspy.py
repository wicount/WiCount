import sqlite3 as sql
from sqlite3 import OperationalError
import json
import os
from dateutil.parser import parse
from datetime import datetime, timedelta


def percentage_utilisation():

    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row # Enables column access by name: row['column_name']

    cur = con.cursor()

    sqlstring = 'SELECT room_id, PredictedPercentage, count(*) as count, room \
                From analytics \
                GROUP BY room_id, PredictedPercentage \
                Order by room_id'

    try:
        percentage = cur.execute(sqlstring).fetchall()
        con.commit()
        return json.dumps([dict(ix) for ix in percentage])

    except OperationalError:
        con.close()
        return "An error occurred while calculating percentage utilisation"
    except Exception as e:
        print(e)


def greater_lesser(numberpeople, comparison):

    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row # Enables column access by name: row['column_name']

    cur = con.cursor()


    if comparison == '>=':
        operator = '>='
    else:
        operator = '<='

    sqlstring = "SELECT room, date\
    FROM analytics \
    WHERE ? {} ((0.1 * PredictedPercentage) * Capacity)".format(operator)

    # Have to use string operation because ">=" is an SQL parameter.

    roomlist = cur.execute(sqlstring, (numberpeople,)).fetchall()
    con.commit()
    return json.dumps([dict(ix) for ix in roomlist])


def list_occupancy_x(occupancy):
    # List rooms where occupancy = 0/50/100
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row # Enables column access by name: row['column_name']

    cur = con.cursor()

    # Select full rooms
    sqlstring = 'SELECT * \
    from analytics \
    WHERE PredictedPercentage = ?'

    try:
        roomlist = cur.execute(sqlstring, (occupancy,)).fetchall()
        con.commit()
        return json.dumps([dict(ix) for ix in roomlist])


    except OperationalError:
        con.close()
        return "An error occurred while fetching rooms of occupancy {}%.".format(occupancy)

    except Exception as e:
        print(e)


# if __name__ == '__main__':
#     # for testing
#     print('Percentage utilisation JSON:\n', percentage_utilisation("B-004"))
#     print('Greater/lesser JSON:\n', greater_lesser(10, '>='))
#     print('List occupancy: JSON\n', list_occupancy_x("50"))


def roomUtilisation():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT room, ROUND(predictions) as predictions FROM analytics GROUP BY room''').fetchall()

    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def timeUtilisation():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT date, ROUND(predictions) as predictions FROM analytics GROUP BY date''').fetchall()

    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def dayUtilisation():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT day, ROUND(predictions) as predictions FROM analytics GROUP BY day''').fetchall()

    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def occupnacyBasedOnTime():
    return 0

def occupnacyBasedOnDay():
    return 0

def percentgeOccupiedRoom():
    con = sql.connect("wicount.sqlite3")
    con.row_factory = sql.Row
    cur = con.cursor()

    rows = cur.execute('''SELECT room FROM analytics GROUP BY room''').fetchall()

    con.commit()
    con.close()

    return json.dumps( [dict(ix) for ix in rows],sort_keys=False)

def percentgeOccupiedTime():
    return 0

def percentgeOccupiedDay():
    return 0

def listEmptyRoom():
    return 0

def listFullRoom():
    return 0

if __name__ == '__main__':

    print(percentgeOccupiedRoom())
