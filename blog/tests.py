from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.cache import cache
from rest_framework.throttling import ScopedRateThrottle

class BlogAPITests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        self.blog_v1_url = '/api/v1/blogs/'
        self.blog_v2_url = '/api/v2/blogs/'

    def test_crud_v1(self):
        # Create
        payload = {"title": "V1 Post", "content": "V1 content"}
        resp = self.client.post(self.blog_v1_url, payload, format='json', **self.auth_header)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        blog_id = resp.data['id']

        # Retrieve
        resp2 = self.client.get(f"{self.blog_v1_url}{blog_id}/", **self.auth_header)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data['title'], "V1 Post")

        # Update
        resp3 = self.client.put(f"{self.blog_v1_url}{blog_id}/", {"title": "Updated", "content": "Updated content"}, format='json', **self.auth_header)
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        self.assertEqual(resp3.data['title'], "Updated")

        # Delete
        resp4 = self.client.delete(f"{self.blog_v1_url}{blog_id}/", **self.auth_header)
        self.assertEqual(resp4.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_v2(self):
        payload = {"title": "V2 Post", "content": "V2 content", "category": "Tech", "tags": "django,api"}
        resp = self.client.post(self.blog_v2_url, payload, format='json', **self.auth_header)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        blog_id = resp.data['id']

        # Check view_count is read-only
        self.assertEqual(resp.data['view_count'], 0)

        # Retrieve
        resp2 = self.client.get(f"{self.blog_v2_url}{blog_id}/", **self.auth_header)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertEqual(resp2.data['category'], "Tech")

        # Update
        resp3 = self.client.put(f"{self.blog_v2_url}{blog_id}/", {"title": "Updated V2", "content": "Updated content", "category": "Science", "tags": "api,rest"}, format='json', **self.auth_header)
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        self.assertEqual(resp3.data['category'], "Science")

        # Delete
        resp4 = self.client.delete(f"{self.blog_v2_url}{blog_id}/", **self.auth_header)
        self.assertEqual(resp4.status_code, status.HTTP_204_NO_CONTENT)

    def test_throttle_limit(self):
        payload = {"title": "Throttle Test", "content": "x"}
        for i in range(5):
            resp = self.client.post(self.blog_v2_url, payload, format='json', **self.auth_header)
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # 6th post should fail
        resp6 = self.client.post(self.blog_v2_url, payload, format='json', **self.auth_header)
        self.assertEqual(resp6.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
