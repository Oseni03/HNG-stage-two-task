from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

User = get_user_model()

class TokenGenerationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            password="password123"
        )

    def test_token_generation(self):
        refresh = RefreshToken.for_user(self.user)
        access = refresh.access_token

        # Check if token expires correctly
        self.assertLessEqual(refresh.access_token.payload['exp'], refresh.payload['exp'])
        self.assertLessEqual(access.lifetime, timedelta(days=5))  # Default expiry for access token

        # Check if correct user tedetails are in token
        self.assertEqual(str(access['user_id']), str(self.user.id))