from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTestCase(APITestCase):
    def test_register(self):
        data = {
            "username":"testuser",
            "email":"testuser@eg.com",
            "password":"mypassword",
            "password2":"mypassword"
        }
        url = reverse('signup')
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser",password="mypassword")

    def test_login(self):
        data = {"username":"testuser",
                "password":"mypassword"
            }
        response = self.client.post(reverse('login'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_logout(self):
        self.token = Token.objects.get(user__username="testuser")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)