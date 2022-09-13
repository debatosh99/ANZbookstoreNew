import unittest
import requests
import dbInitializer
import app

class TestApp(unittest.TestCase):

    #baseurl = 'http://127.0.0.1:5000/v1/books'
    baseurl = 'http://192.168.0.110:8080/v1/books'
    testbook1 = {"name":"Atomic Habits", "author": "Mr India", "published_date": "22/09/07", "price": 700, "in_stock": "Yes"}

    def setUp(self) -> None:
        dbInitializer.createDBandTable("Library2.db")
        dbInitializer.insertSampleRecords()
        dbInitializer.printAllRecords()
        dbInitializer.filterAndGetJson()

    def test_get_book(self):
        res1 = requests.get(TestApp.baseurl)
        self.assertEqual(res1.status_code, 200)
        res2 = requests.get(TestApp.baseurl+'/')
        self.assertEqual(res2.status_code, 404)

    def test_create_book(self):
        res = requests.post(TestApp.baseurl, json=TestApp.testbook1)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json()['id'], int)
        res = requests.post(TestApp.baseurl, json=TestApp.testbook1)
        self.assertEqual(res.status_code, 403)

    def test_get_books(self):
        res = requests.get(TestApp.baseurl+'?name="Math*"')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(len(res.json()), int)

    def test_get_matching_books(self):
        res1 = requests.get(TestApp.baseurl+'/1')
        res2 = requests.get(TestApp.baseurl + '/0')
        self.assertEqual(res1.status_code, 200)
        self.assertIsInstance(len(res1.json()), int)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(len(res2.json()), 0)

    def test_dbutil(self):
        customsql = "SELECT count(*) FROM bookstore WHERE name = '{}'".format(str("vague"))
        fetch = 'one'
        result = app.dbutils(customsql, fetch)
        self.assertEqual(result, 0)





if __name__ == '__main__':
#    dosetup()
    unittest.main()




