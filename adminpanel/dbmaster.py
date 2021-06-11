import pymysql
from django.shortcuts import render
from json import dumps
from django.db import connection
#nostring le chai website ma use garana string banaidinxa dictionary lai
def db_reader(db_name,cols,nostring = 0):
    db = pymysql.connect("localhost","root","","neadata" )
    cursor = db.cursor()
    #DB bata padhna chainxa yo
    twod_list = []
    new = []
    sql = "SELECT * FROM %s" % (db_name)       #database ko nam kileni number narakhnu
    i = 0
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for rough in range(cols):
               new.append(row[rough])
            twod_list.append(new)
            new = []
            i +=1

    except:
        print("Error: unable to fecth data")

    db.close()
    if nostring==0:
        dataDictionary = {
            'list2d': twod_list,
            'howmany': i
        }
        dataJSON = dumps(dataDictionary)
        return dataJSON
    else:
        return twod_list,i


def db_reader_hourly(db_name,nostring = 0):
    db = pymysql.connect("localhost","root","","neadata" )
    cursor = db.cursor()
    #DB bata padhna chainxa yo
    twod_list = []
    new = []
    try:
        sql = "SELECT * FROM %s" % (db_name)       #database ko nam kileni number narakhnu
    except:
        return 0;
    i = 0
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            for rough in range(30):
                if (rough!=0 and rough!=7 and rough !=9 and rough !=20 and rough!=22 and rough !=24):
                    new.append(row[rough])
            twod_list.append(new)
            new = []
            i +=1

    except:
        print("Error: unable to fecth data")

    db.close()
    if nostring==0:
        dataDictionary = {
            'list2d': twod_list,
            'howmany': i
        }
        dataJSON = dumps(dataDictionary)
        return dataJSON
    else:
        return twod_list,i



def db_table_exists(db_name):
    try:
        db = pymysql.connect("localhost", "root", "", "neadata")
        cursor = db.cursor()
        # DB bata padhna chainxa yo
        sql = "SELECT * FROM %s" % (db_name)  # database ko nam kileni number narakhnu
        cursor.execute(sql)
        return True
    except:
        return False

