from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from postings.models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    
    def setUp(self):
        user_obj=User(
            username="nomi",
            email="nomi@imfaisal.com",
            )
        user_obj.set_password("nomi1234")
        user_obj.save()


        blog_obj=BlogPost.objects.create(
            user=user_obj,
            title="Api Test",
            content="Some Content for testing",
        )


    def test_single_user(self):
        user_count= User.objects.count()
        self.assertEqual(user_count,1)

    def test_single_post(self):
        post_count= BlogPost.objects.count()
        self.assertEqual(post_count,1)
    
    def test_get_list(self):
        data = {}
        url = api_reverse("api_post:post_create")
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # print(response.data)

    
    def test_post_item(self):
        data = {
            'title':'test title',
            'content':'test content'
            }
        url = api_reverse("api_post:post_create")
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    

    def test_get_item(self):
        post = BlogPost.objects.first()
        data = {}
        url = post.get_api_url()
        response = self.client.get(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        # print(response.data)

    
    def test_update_item(self):
        post=BlogPost.objects.first()
        data = {
            'title':'test title',
            'content':'test content'
            }
        url = post.get_api_url()
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

        # response = self.client.put(url,data,format='json')
        # self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    
    def test_update_item_with_user(self):
        post=BlogPost.objects.first()
        data = {
            'title':'test title',
            'content':'test content'
            }
        url = post.get_api_url()

        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_resp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+token_resp)

        response = self.client.put(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_post_item_with_user(self):
        data = {
            'title':'test title',
            'content':'test content'
            }
        url = api_reverse("api_post:post_create")

        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_resp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+token_resp)


        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    
    def test_user_ownership(self):

        owner=User(username="nomi123")
        owner.save()

        post=BlogPost.objects.create(
            user=owner,
            title="Api Test121",
            content="Some Content for testing12",
        )

        

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username,owner.username)

        payload = payload_handler(user_obj)
        token_resp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT '+token_resp)


        data = {
            'title':'test title',
            'content':'test content'
            }
        url = post.get_api_url()

        response = self.client.put(url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    
    def test_user_login(self):
        data={
            'username':'nomi',
            'password':'nomi1234'
        }

        url = api_reverse("api_login")
        response = self.client.post(url,data)
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        token = response.data.get("token")

        if token is not None:
            post=BlogPost.objects.first()
            data = {
                'title':'test title',
                'content':'test content'
                }
            url = post.get_api_url()

            
            self.client.credentials(HTTP_AUTHORIZATION='JWT '+token)

            response = self.client.put(url,data,format='json')
            self.assertEqual(response.status_code,status.HTTP_200_OK)


