import json
from django.test import TestCase
from ponto.models import CustomUser as User, Group as Setor


class ModelsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user_test = User.objects.create_user(
            matricula='197623',
            password='root12345',
            email='mr.mraulino@gmail.com',
            first_name='user',
            last_name='teste'
        )

    def testCreateUser(self):
        user_1 = User.objects.create_user(
            matricula='178934',
            password='root12345',
            email='mr.mraulino@gmail.com',
            first_name='Mateus',
            last_name='Raulino'
        )
        self.assertEqual(User.objects.all().count(), 2)
        self.assertIsNotNone(User.objects.filter(first_name='Mateus', last_name='Raulino'))
    
    def testUpdateUser(self):
        User.objects.update(
            id=self.user_test.id,
            matricula='123456', 
            first_name='Raulino', 
            last_name='Mateus'
            )
        user = User.objects.get(matricula='123456')
        self.assertEqual(user.id, self.user_test.id)
        self.assertEqual(user.first_name, 'Raulino')
        self.assertEqual(user.last_name, 'Mateus')
        self.assertEqual(user.matricula, '123456')
        self.assertEqual(user.email, 'mr.mraulino@gmail.com')
    
    def testReadUser(self):
        user = User.objects.get(matricula='197623')
        self.assertEqual(user.first_name, 'user')
        self.assertEqual(user.last_name, 'teste')
        self.assertEqual(user.matricula, '197623')
        self.assertEqual(user.email, 'mr.mraulino@gmail.com')
        
    def testDeleteUser(self):
        user = User.objects.get(matricula='197623')
        user.delete()
        self.assertEqual(User.objects.all().count(), 0)
