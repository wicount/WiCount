import sqlite3 as sql
from sqlite3 import OperationalError


def percentage_utilisation():

    con = sql.connect("wicount.sqlite3")
    cur = con.cursor()

    sqlstring = 'SELECT DISTINCT room, (CAST (COUNT(room) AS FLOAT) / \
        (SELECT DISTINCT COUNT(room) FROM analytics) *100) AS PercentageUtilised \
        FROM analytics \
        WHERE PredictedPercentage > 0'

    try:
        percentage = cur.execute(sqlstring).fetchall()
        con.commit()
        return percentage

    except OperationalError:
        con.close()
        return "An error occurred while calculating percentage utilisation"
    except Exception as e:
        print(e)


def greater_lesser(numberpeople, comparison):

    con = sql.connect("wicount.sqlite3")
    cur = con.cursor()

    if comparison == '>=':
        operator = '>='
    else:
        operator = '<='

    sqlstring = 'SELECT room, date\
    FROM analytics \
    WHERE ' + str(numberpeople) + str(operator) + '((0.1 * PredictedPercentage) * Capacity)'

    try:
        roomlist = cur.execute(sqlstring).fetchall()
        con.commit()
        return roomlist

    except OperationalError:
        con.close()
        return "An error occurred while fetching the requested rooms."

    except Exception as e:
        print(e)


def list_occupancy_x(x):
    # List rooms where occupancy = 0/50/100
    con = sql.connect("wicount.sqlite3")
    cur = con.cursor()

    # Select full rooms
    sqlstring = 'SELECT room, date, Module \
    from analytics \
    WHERE PredictedPercentage ='+str(x)

    try:
        roomlist = cur.execute(sqlstring).fetchall()
        con.commit()
        return roomlist

    except OperationalError:
        con.close()
        return "An error occurred while fetching rooms of occupancy {}%.".format(x)

    except Exception as e:
        print(e)


print(percentage_utilisation())
print(greater_lesser(10, '>='))
print('List occupancy:', list_occupancy_x(50))

