import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "test1234"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.get_json())

    def test_create_user_invalid_email(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "test1234"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_name(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "janedoe@gmail.com",
            "password": "test1234"
        })
        self.assertEqual(response.status_code, 400)
