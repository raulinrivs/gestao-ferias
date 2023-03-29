import json
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from ponto.models import CustomUser as User, Group as Setor


class AccountsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.url = '127.0.0.1:8000/api/v1/accounts'
        cls.client = APIRequestFactory()
        cls.user_test = User.objects.create_user(
            matricula='197623',
            password='root12345',
            email='mr.mraulino@gmail.com',
            first_name='user',
            last_name='teste'
        )

    def testLoginLogoutEndpoint(self):
        response = self.client.post(
            path='/api/v1/accounts/login/',
            data={
                'username': '197623',
                'password': 'root12345',
            }
            )
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.cookies['csrftoken'])
        self.assertIsNotNone(response.cookies['sessionid'])
        response = self.client.get(
            path='/api/v1/accounts/logout/'
        )
        self.assertEqual(response.status_code, 200)

    # def testPasswordChange(self):
    #     response = self.client.post(
    #         path='/api/v1/accounts/login/',
    #         data={
    #             'username': '197623',
    #             'password': 'root12345',
    #         }
    #         )
    #     response = self.client.put(
    #         path='/api/v1/accounts/password_change/',
    #         data=json.dumps({
    #             'password': 'root12345',
    #             'new_password': '12345root',
    #             'new_password_confirm': '12345root'
    #         }),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(self.user_test.check_password('12345root'))
