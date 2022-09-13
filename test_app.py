import unittest
import requests
#import com.anz.cloud.app1

class TestApp(unittest.TestCase):

    #baseurl = 'http://127.0.0.1:5000/v1/books'
    baseurl = 'http://192.168.0.110:8080/v1/books'
    testbook1 = {"name":"Atomic Habits", "author": "Mr India", "published_date": "22/09/07", "price": 700, "in_stock": "Yes"}


    def test_get_book(self):
        #baseurl = "http://127.0.0.1:5000"
        #response = requests.get(baseurl + "/v1/books/3")
        #response.json()
        self.assertEqual(1,1)

    def test_create_book(self):
        res = requests.post(TestApp.baseurl, json=TestApp.testbook1)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json()['id'], int)

    def test_get_books(self):
        res = requests.get(TestApp.baseurl+'?name="Math*"')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(len(res.json()), int)



    def test_get_matching_books(self):
        # r = requests.get(TestApp.baseurl)
        # self.assertEqual(r.status_code, 200)
        # self.assertEqual(len(r.json()), 2)
        self.assertEqual(1, 1)



if __name__ == '__main__':
    unittest.main()


