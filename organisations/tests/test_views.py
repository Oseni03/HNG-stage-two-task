from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class OrganisationEndpointTest(APITestCase):

    def setUp(self):
        self.organisation1_data = {
            "name": "Org 1",
            "description": "Org 1 description",
        }
        self.organisation2_data = {
            "name": "Org 2",
            "description": "Org 2 description",
        }
        self.organisation3_data = {
            "name": "Org 3",
            "description": "Org 3 description",
        }
        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "password": "bcbhwyeuqwe894rb8323jh1",
        }
        self.login_cred = {
            "email": "john.doe@example.com",
            "password": "bcbhwyeuqwe894rb8323jh1",
        }

        self.register_url = reverse("users:register")
        self.login_url = reverse("users:login")
        self.create_org_url = reverse("organisations:list-create-organisation")

    def test_user_organisation(self):
        user = self.client.post(self.register_url, self.user_data, format="json")
        user_id = user.data["data"]["user"]["user_id"]

        login = self.client.post(self.login_url, self.login_cred, format="json")
        organisation1 = self.client.post(
            self.create_org_url, self.organisation1_data, format="json"
        )
        organisation2 = self.client.post(
            self.create_org_url, self.organisation2_data, format="json"
        )
        organisation3 = self.client.post(
            self.create_org_url, self.organisation3_data, format="json"
        )

        org1_id = organisation1.data["data"]["org_id"]
        org2_id = organisation2.data["data"]["org_id"]
        org3_id = organisation3.data["data"]["org_id"]

        response = self.client.post(
            reverse("organisations:add-user", args=(org1_id,)),
            {"user_id": user_id},
            format="json",
        )
        response = self.client.post(
            reverse("organisations:add-user", args=(org2_id,)),
            {"user_id": user_id},
            format="json",
        )

        organisations = self.client.get(
            reverse("users:user-organisations", args=(user_id,)),
            self.user_data,
            format="json",
        )
        organisation_list = organisations.data["data"]["organisations"]
        # if the user actually had access to all the organisations, 
        # then the total number of the user organisations will be 4 
        # because of the default organisation created along with the user
        self.assertEqual(len(organisation_list), 3)
