from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

URL = "/api/products/"
GOOD = {"name": "Notebook", "description": "A notebook with 100 pages.", "price": "120.00", "stock": 25}


class ProductAPITests(APITestCase):
    def setUp(self):
        user = User.objects.create_user("testuser", password="testpass123")
        self.token = Token.objects.create(user=user).key

    def auth(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_empty_list_is_paginated(self):
        r = self.client.get(URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["results"], [])

    def test_create_with_token(self):
        self.auth()
        r = self.client.post(URL, GOOD, format="json")
        self.assertEqual(r.status_code, 201)
        self.assertIn("id", r.data)

    def test_create_without_token_denied(self):
        self.assertEqual(self.client.post(URL, GOOD, format="json").status_code, 401)

    def test_invalid_data(self):
        self.auth()
        for bad in [{"name": ""}, {"name": "   "}, {"price": "0"}, {"price": "-5"},
                    {"stock": -1}, {"stock": 2.5}]:
            r = self.client.post(URL, {**GOOD, **bad}, format="json")
            self.assertEqual(r.status_code, 400, bad)

    def test_page_two_has_sixth_product(self):
        self.auth()
        for i in range(1, 7):
            self.client.post(URL, {**GOOD, "name": f"Item {i}"}, format="json")
        self.client.credentials()
        r = self.client.get(URL + "?page=2")
        self.assertEqual(r.status_code, 200)
        self.assertEqual([p["name"] for p in r.data["results"]], ["Item 6"])
