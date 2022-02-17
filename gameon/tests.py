from django.contrib.auth.models import User
from django.http import response
from django.urls import reverse

from gameon.models import StreamPlatform, WatchList, Review
from gameon.api import serializers
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase

class StreamPlatformTestCase(APITestCase):
     
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(
            name='Netflix',about='standard streaming',website='http://netflix.org'
        )

    def test_stream_platform_create(self):
        data = {
            'name': 'netflix',
            'about':'standard stream service',
            'website': 'http://netfilx.com'
        }
        response = self.client.post(reverse('streamplatform'))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_stream_platform_list(self):
        response = self.client.get(reverse('streamplatform'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_stream_platform_ind(self):
        response = self.client.get(reverse('streamplatform_detail',args=(self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test',password='test123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(
            name='Netflix',about='standard streaming',website='http://netflix.org'
        )
        self.watchlist = WatchList.objects.create(
            platform=self.stream,title='the boy',storyline='the boy survived and he said Alhamdulilah',active=True
            )            

    def test_watch_list_create(self):
        data = {
            'name': 'the boy',
            'storyline':'the boy later grew up',
            'platform': self.stream,
            'active': True
        }

        response = self.client.post(reverse('watchlist'), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def  test_watch_list_ind(self):
        response = self.client.get(reverse('watchlist_detail',args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test123')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = StreamPlatform.objects.create(
            name='Netflix',about='standard streaming',website='http://netflix.org'
        )
        self.watchlist = WatchList.objects.create(
            platform=self.stream,title='the boy',storyline='the boy survived and he said Alhamdulilah',active=True
            )   
        self.review = Review.objects.create(
            review_user=self.user,rating=4,description='good movie',active=True,watchlist=self.watchlist
        )

    def test_review_create(self):
        data = {
            'review_user':self.user,
            'rating': 5,
            'description': 'greate movie',
            'active': True,
            'watchlist': self.watchlist,
         }
        response = self.client.post(reverse('review-create',args=(self.watchlist.pk,)),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_review_unauthenticated(self):
        data = {
            'review_user':self.user,
            'rating': 5,
            'description': 'greate movie',
            'active': True,
            'watchlist': self.watchlist,
         }

        self.client.force_authenticate(user=None)
        response = self.client.post(reverse('review-create',args=(self.watchlist.pk,)),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_review_list(self):
        response = self.client.get(reverse('review-list',args=(self.watchlist.pk,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review_detail',args=(self.review.pk,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_update(self):
        data = {
            'review_user':self.user,
            'rating': 5,
            'description': 'greate movie',
            'active': True,
            'watchlist': self.watchlist,
         }
        response = self.client.put(reverse('review_detail',args=(self.review.pk,)),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_user(self):
        response = self.client.get('watch/review/?username='+ self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        

