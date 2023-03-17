from typing import Any
from django.test import TestCase
from ponto.models import CustomUser as User, Group


class UserTest(TestCase):
    """ Test module for CustomUser model """

    def setUp(self):
        group_ti = Group.objects.create(name='TI')
        group_financeiro = Group.objects.create(name='Financeiro')
        group_rh = Group.objects.create(name='Recursos Humanos')
        group_ti.user_set.add(User.objects.create(username='colaborador_1', first_name='colaborador', last_name='um', password='root12345', matricula='111111'))
        group_ti.user_set.add(User.objects.create(username='gestor_ti', first_name='gestor', last_name='ti', password='root12345', matricula='111113', gestor=group_ti))
        group_financeiro.user_set.add(User.objects.create(username='colaborador_2', first_name='colaborador', last_name='dois', password='root12345', matricula='111112'))
        group_financeiro.user_set.add(User.objects.create(username='gestor_financeiro', first_name='gestor', last_name='financeiro', password='root12345', matricula='111114'))
        group_rh.user_set.add(User.objects.create(username='rh_1', first_name='recursos humanos', last_name='um', password='root12345', matricula='111115'))
        group_rh.user_set.add(User.objects.create(username='gestor_rh', first_name='gestor', last_name='recursos humanos', password='root12345', matricula='111116'))
        
    def test_user(self):
        colaborador_1 = User.objects.get(username='colaborador_1')
        colaborador_2 = User.objects.get(username='colaborador_2')
        rh_1 = User.objects.get(username='rh_1')
        
        
