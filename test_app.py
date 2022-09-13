import unittest
import requests
#import com.anz.cloud.app1

class TestApp(unittest.TestCase):

    #baseurl = 'http://127.0.0.1:5000/v1/books'
    baseurl = 'http://192.168.0.110:8080/v1/books'
    testbook1 = {"name":"Atomic Habits", "author": "Mr India", "published_date": "22/09/07", "price": 700, "in_stock": "Yes"}


    def test_get_book(self):
        res = requests.get(TestApp.baseurl)
        self.assertEqual(res.status_code, 200)

    def test_create_book(self):
        res = requests.post(TestApp.baseurl, json=TestApp.testbook1)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.json()['id'], int)

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




if __name__ == '__main__':
    unittest.main()


