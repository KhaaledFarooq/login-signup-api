import unittest
from app import app

class AppTestCase(unittest.TestCase):
    global token
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_register_endpoint(self):
        # Sending a POST request to the register endpoint with valid data
        response = self.app.post('/register', json={'username': 'test_user10', 'password': 'test_password'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['message'], 'User registered successfully')

        # Sending a POST request with missing data
        response = self.app.post('/register', json={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Missing username or password')

    def test_login_endpoint(self):
        # Sending a POST request to the login endpoint with valid credentials
        response = self.app.post('/login', json={'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        global token
        token = response.json['token']

        # Sending a POST request with invalid credentials
        response = self.app.post('/login', json={'username': 'test_user', 'password': 'wrong_password'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Invalid username or password')

    def test_protected_page_endpoint(self):
        # Sending a GET request to the protected-page endpoint with a valid access token
        global token
        response = self.app.get('/protected-page?token='+token)
        self.assertEqual(response.status_code, 200)

        # Sending a GET request without an access token
        response = self.app.get('/protected-page')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['message'], 'Access token missing')


if __name__ == '__main__':
    unittest.main()
