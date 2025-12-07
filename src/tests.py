import unittest
# src/tests.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import app as tested_app
import json

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        tested_app.app.config['TESTING'] = True
        self.app = tested_app.app.test_client()
    
    def tearDown(self):
        super().tearDown()
        with open('src/data.json', 'w') as f:
            json.dump([], f)

    def test_get_hello_endpoint(self):
        r = self.app.get('/')
        self.assertEqual(r.data, b'Hello World!')

    def test_post_hello_endpoint(self):
        r = self.app.post('/')
        self.assertEqual(r.status_code, 405)

    def test_get_api_endpoint(self):
        r = self.app.get('/api')
        self.assertEqual(r.json, {'status': 'test'})

    def test_correct_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'name': 'Den', 'age': 100}))
        self.assertEqual(r.json, {'status': 'OK'})
        self.assertEqual(r.status_code, 200)

        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'name': 'Den'}))
        self.assertEqual(r.json, {'status': 'OK'})
        self.assertEqual(r.status_code, 200)

    def test_not_dict_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps([{'name': 'Den'}]))
        self.assertEqual(r.json, {'status': 'bad input'})
        self.assertEqual(r.status_code, 400)

    def test_no_name_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'age': 100}))
        self.assertEqual(r.json, {'status': 'bad input'})
        self.assertEqual(r.status_code, 400)

    def test_bad_age_post_api_endpoint(self):
        r = self.app.post('/api',
                          content_type='application/json',
                          data=json.dumps({'name': 'Den', 'age': '100'}))
        self.assertEqual(r.json, {'status': 'bad input'})
        self.assertEqual(r.status_code, 400)

    def test_add_success(self):
        r = self.app.get('/add?a=2&b=3')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data, b'5.0')
    
    def test_add_transaction_validation_error(self):
        create_data = {
            'amount': 500.0,
            'payer': 121314324142,
            'recipient': '3333333333233',
        }

        response = self.app.post('/transactions/', content_type='application/json', data=json.dumps(create_data))

        self.assertEqual(response.status_code, 400)
    
    def test_add_transaction_success(self):
        create_data = {
            'amount': 500.0,
            'payer': '121314324142',
            'recipient': '3333333333',
        }

        response = self.app.post('/transactions/', content_type='application/json', data=json.dumps(create_data))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'message': 'Транзакция успешно добавлена'})

        response_list = self.app.get('/transactions/')
        self.assertEqual(response_list.status_code, 200)
        self.assertEqual(len(response_list.json), 1)

##
###
if __name__ == '__main__':
    unittest.main()