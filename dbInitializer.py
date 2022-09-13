import sqlite3
from datetime import datetime
import json


##################################################################################
# CREATE BASIC SQLLITE DB AND TABLE
##################################################################################
def createDBandTable(dbname):
    dbname = dbname
    try:
        print(".....CREATE BASIC SQLLITE DB AND TABLE.....")
        con = sqlite3.connect(dbname)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS bookstore")

        mysql = '''CREATE TABLE "bookstore" (
        	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
        	"name"	TEXT,
        	"author"	TEXT,
        	"published_date"	DATE,
        	"price"	REAL,
        	"in_stock" TEXT
        )'''
        cur.execute(mysql)
        con.commit()

    except sqlite3.Error as error:
        print("SQL Error", error)

    except Exception as exp:
        print("DB connection failed")

    else:
        print(".....DONE.....")

    finally:
        con.close()
##################################################################################




##################################################################################
# INSERT FEW RECORDS IN THE SQLLITE TABLE
##################################################################################
def insertSampleRecords():
    try:
        print(".....INSERT FEW RECORDS IN THE SQLLITE TABLE.....")
        con = sqlite3.connect('Library2.db')
        cur = con.cursor()

        date_1 = datetime.strptime('22/09/01', '%y/%m/%d')
        date_2 = datetime.strptime('22/09/02', '%y/%m/%d')
        date_3 = datetime.strptime('22/09/03', '%y/%m/%d')
        date_4 = datetime.strptime('22/09/04', '%y/%m/%d')

        records = [('Science basics', 'Mr Ravi', date_1, 100, 'Yes'),
                   ('Physics basics', 'Mr Suresh', date_2, 200, 'No'),
                   ('Math basics', 'Miss Rima', date_3, 300, 'Yes'),
                   ('Arts basics', 'Miss Sia', date_4, 400, 'No')]

        cur.executemany('INSERT INTO bookstore (name,author,published_date,price,in_stock) VALUES(?,?,?,?,?);',
                        records);
        con.commit()

    except sqlite3.Error as error:
        print("SQL Error", error)

    except Exception as exp:
        print("DB connection failed")

    else:
        print(".....DONE.....")
    finally:
        con.close()
##################################################################################



##################################################################################
# SELECT ALL THE RECORDS FROM THE SQLLITE TABLE AND PRINT
##################################################################################
def printAllRecords():
    try:
        print(".....SELECT ALL THE RECORDS FROM THE SQLLITE TABLE AND PRINT.....")
        con = sqlite3.connect('Library2.db')
        cur = con.cursor()
        mysql = "SELECT * FROM bookstore"
        # cur.execute("SELECT * FROM bookstore WHERE id = ?", [int(book_id)])
        # cur.execute("SELECT * FROM bookstore WHERE publisher like 'mem%'")
        cur.execute(mysql)
        # print(cur.fetchone())
        print(cur.fetchall())

    except sqlite3.Error as error:
        print("SQL Error", error)

    except Exception as exp:
        print("DB connection failed")

    else:
        print(".....DONE.....")
    finally:
        con.close()
##################################################################################



##################################################################################
# SELECT RECORD BASED ON FILTER CRITERIA AND PRINT JSON
##################################################################################
def filterAndGetJson():
    try:
        print(".....SELECT RECORD BASED ON FILTER CRITERIA AND PRINT JSON.....")
        book_id = 1
        con = sqlite3.connect("Library2.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM bookstore WHERE id = ?", [int(book_id)])
        # data = cur.fetchone()
        result = [dict(row) for row in cur.fetchall()]
        print(json.dumps(result))

    except sqlite3.Error as error:
        print("SQL Error", error)

    except Exception as exp:
        print("DB connection failed")

    else:
        print(".....DONE.....")
    finally:
        con.close()
##################################################################################


if __name__ == '__main__':
    createDBandTable("Library2.db")
    insertSampleRecords()
    printAllRecords()
    filterAndGetJson()
