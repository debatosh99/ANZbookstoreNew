import json

from flask import Flask, jsonify, request, url_for
from http import HTTPStatus
import sqlite3 as sql
from datetime import datetime
import config as config


app = Flask(__name__)

def dbutils(customsql, fetch):
    try:
        con = sql.connect("Library2.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        print(".............................")
        print(customsql)
        cur.execute(customsql)
        con.commit()
        if fetch == 'all':
            result = [dict(row) for row in cur.fetchall()]
        else:
            result = cur.fetchone()[0]
    except sql.Error as error:
        print("SQL Error", error)
        return jsonify({"message": "Retry after sometime"}), HTTPStatus.SERVICE_UNAVAILABLE
    except Exception as exp:
        print("DB connection failed")
        return jsonify({"message": "Retry after sometime"}),HTTPStatus.SERVICE_UNAVAILABLE
    else:
        print("DB connection success")
        print(result)
        return result
    finally:
        con.close()



@app.route('/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    customsql = "SELECT * FROM bookstore WHERE id = {}".format(int(book_id))
    fetch = 'all'
    result = dbutils(customsql, fetch)
    if result is None:
        return jsonify({"message": "Book not found"}),HTTPStatus.NOT_FOUND
    else:
        json_output = json.dumps(result)
        return jsonify(result), 200



@app.route('/v1/books', methods=['POST'])
def create_book():
    data = request.json
    print(data)
    name = data.get('name')
    author = data.get('author')
    published_date_user = data.get('published_date')
    published_date = datetime.strptime(published_date_user, '%y/%m/%d')
    price = data.get('price')
    in_stock = data.get('in_stock')

    # Check if the record with same book name is already present in the DB
    customsql = "SELECT count(*) FROM bookstore WHERE name = '{}'".format(str(name))
    fetch = 'one'
    result = dbutils(customsql, fetch)
    if result != 0:
        return jsonify({"message": "Book already present"}), HTTPStatus.FORBIDDEN

    # If the record is a new record not present in DB then insert into DB
    customsql = "insert into bookstore(name,author,published_date,price,in_stock) values ('{}','{}','{}',{},'{}')".format(name, author, published_date, price, in_stock)
    fetch = 'one'
    result = dbutils(customsql, fetch)

    # Get the id of the newly inserted record
    customsql = "SELECT id FROM bookstore WHERE name = '{}'".format(str(name))
    fetch = 'one'
    id = dbutils(customsql, fetch)
    print(id)
    return jsonify({"id": id}), 200




@app.route('/v1/books', methods=['GET'])
def get_books():
    print(len(request.args))
    if len(request.args) == 0:
        customsql = "SELECT * FROM bookstore"
        fetch = 'all'
        result = dbutils(customsql, fetch)
        json_output = json.dumps(result)
        return json_output, 200
    else:
        name = request.args.get('name')
        name = name.replace('*', '%')
        customsql = "SELECT * FROM bookstore WHERE name like {}".format(name)
        fetch = 'all'
        result = dbutils(customsql, fetch)
        if result is None:
            return jsonify({"message": "Book not found"}), HTTPStatus.NOT_FOUND
        else:
            print(result)
            json_output = json.dumps(result)
            return jsonify(result), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
