from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from organisations.models import Organisation

User = get_user_model()


class RegisterEndpointTest(APITestCase):

    def setUp(self):
        self.user_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "password": "bcbhwyeuqwe894rb8323jh1",
        }

        self.register_url = reverse("users:register")

    def test_register_user_successfully(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access_token", response.data["data"])
        self.assertEqual(
            response.data["data"]["user"]["firstName"], self.user_data["firstName"]
        )
        self.assertEqual(
            response.data["data"]["user"]["email"], self.user_data["email"]
        )

    def test_register_user_with_default_organisation(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user_id = int(response.data["data"]["user"]["userId"])
        organisation = Organisation.objects.filter(users__id=user_id).first()
        self.assertIsNotNone(organisation)
        self.assertEqual(
            organisation.name, f"{self.user_data['firstName']}'s Organisation"
        )

    def test_register_user_missing_fields(self):
        missing_fields_data = {
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "password": "EN;WFNJWED78123",
        }
        response = self.client.post(
            self.register_url, missing_fields_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("firstName", response.data["errors"][0]["field"])

    def test_register_user_duplicate_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("email", response.data["errors"][0]["field"])