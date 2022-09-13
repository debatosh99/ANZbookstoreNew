import json

from flask import Flask, jsonify, request, url_for
from http import HTTPStatus
import sqlite3 as sql
from datetime import datetime
import config as config


app = Flask(__name__)


@app.route('/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    try:
        con = sql.connect("Library2.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM bookstore WHERE id = ?", [int(book_id)])
        #data = cur.fetchone()
        result = [dict(row) for row in cur.fetchall()]
        #print(result)
    except sql.Error as error:
        print("SQL Error", error)
        return jsonify({"message": "Retry after sometime"}), HTTPStatus.SERVICE_UNAVAILABLE
    except Exception as exp:
        print("DB connection failed")
        return jsonify({"message": "Retry after sometime"}),HTTPStatus.SERVICE_UNAVAILABLE
    else:
        print("DB connection success")
    finally:
        con.close()

    if result is None:
        return jsonify({"message": "Book not found"}),HTTPStatus.NOT_FOUND
    else:
        json_output = json.dumps(result)
        return jsonify(result), 200
        #return jsonify(result), 200


@app.route('/v1/books', methods=['POST'])
def create_book():
    data = request.json
    #data = request.form.to_dict()
    print(data)
    #data = json.loads(request.form.get('data'))
    #data = request.get_json()
    name = data.get('name')
    author = data.get('author')
    published_date_user = data.get('published_date')
    published_date = datetime.strptime(published_date_user, '%y/%m/%d')
    price = data.get('price')
    in_stock = data.get('in_stock')

    try:
        con = sql.connect("Library2.db")
        cur = con.cursor()
        cur.execute("insert into bookstore(name,author,published_date,price,in_stock) values (?,?,?,?,?)", (name, author, published_date, price, in_stock))
        con.commit()
        cur.execute("SELECT id FROM bookstore WHERE name = ?", [str(name)])
        id = cur.fetchone()[0]
        print(id)
    except sql.Error as error:
        print("SQL Error", error)
        return jsonify({"message": "Retry after sometime"}), HTTPStatus.SERVICE_UNAVAILABLE
    except Exception as exp:
        print("DB connection failed")
        return jsonify({"message": "Retry after sometime"}),HTTPStatus.SERVICE_UNAVAILABLE
    else:
        print("DB connection success")
    finally:
        con.close()

    return jsonify({"id":id}), 200


@app.route('/v1/books', methods=['GET'])
def get_books():
    print(len(request.args))
    if len(request.args) == 0:
        try:
            con = sql.connect("Library2.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM bookstore")
            result = [dict(row) for row in cur.fetchall()]
            #data = cur.fetchall()
        except sql.Error as error:
            print("SQL Error", error)
            return jsonify({"message": "Retry after sometime"}), HTTPStatus.SERVICE_UNAVAILABLE
        except Exception as exp:
            print("DB connection failed")
            return jsonify({"message": "Retry after sometime"}), HTTPStatus.SERVICE_UNAVAILABLE
        else:
            print("DB connection success")
        finally:
            con.close()

        json_output = json.dumps(result)
        return json_output, 200
    else:
        name = request.args.get('name')
        name = name.replace('*', '%')
        try:
            con = sql.connect("Library2.db")
            con.row_factory = sql.Row
            cur = con.cursor()
            query = "SELECT * FROM bookstore WHERE name like {}".format(name)
            cur.execute(query)
            result = [dict(row) for row in cur.fetchall()]
            #data = cur.fetchall()
        except sql.Error as error:
            print("SQL Error", error)
            return jsonify({"message": "Retry after sometime"}), HTTPStatus.SERVICE_UNAVAILABLE
        except Exception as exp:
            print("DB connection failed")
            return jsonify({"message": "Retry after sometime"}), HTTPStatus.SERVICE_UNAVAILABLE
        else:
            print("DB connection success")
        finally:
            con.close()

        if result is None:
            return jsonify({"message": "Book not found"}), HTTPStatus.NOT_FOUND
        else:
            print(result)
            json_output = json.dumps(result)
            return jsonify(result), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)
