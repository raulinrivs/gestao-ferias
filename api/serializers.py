from base64 import urlsafe_b64decode
import json
from rest_framework import serializers
from datetime import datetime, date, time
from ponto.models import CustomUser as User, Solicitacao, Setor
from api.validators import validador_ferias_integral, validador_ferias_venda, \
    validador_ferias_parcial
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'matricula', 'data_admissao')


'''
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'matricula', 'email', 'groups')
'''


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('matricula', 'email')


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate_matching_password(self, value):
        if value['new_password'] != value['new_password_confirm']:
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ['id', 'name']


class SolicitacaoSerializer(serializers.ModelSerializer):
    solicitante = UserDashboardSerializer(many=False, read_only=True)

    class Meta:
        model = Solicitacao
        fields = '__all__'

    def validate(self, attrs):
        if self.instance:
            intervalos = json.loads(self.instance.intervalos)
            tipo_ferias = self.instance.tipo_ferias
        else:
            intervalos = json.loads(attrs.get('intervalos'))
            tipo_ferias = attrs.get('tipo_ferias')
        for chave, valor in intervalos.items():
            intervalos[chave] = datetime.strptime(valor, '%d/%m/%Y')
        data_hoje = datetime.combine(date.today(), time(0, 0))

        if tipo_ferias == 'INT':
            validador_ferias_integral(
                intervalos['data_inicial_1'], intervalos['data_final_1'],
                data_hoje
            )
        elif tipo_ferias == 'VEN':
            validador_ferias_venda(
                intervalos['data_inicial_1'], intervalos['data_final_1'],
                intervalos['data_inicial_venda'], intervalos['data_final_venda'])
        elif tipo_ferias == 'PAR':
            validador_ferias_parcial(
                intervalos['data_inicial_1'], intervalos['data_final_1'],
                intervalos['data_inicial_2'], intervalos['data_final_2'],
                intervalos['data_inicial_3'], intervalos['data_final_3'])
        return super().validate(attrs)


class RestPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ('email')

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            if User.objects.exists(email=email):
                return super().validate(attrs)
        except:
            print('deu ruim')


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ('password', 'token', 'uidb64')

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = smart_str(urlsafe_b64decode(uidb64))
            user = User.objects.filter(id=id).first()

            if not PasswordResetTokenGenerator().check_token(user, token):
                print('falho')

            user.set_password(password)
            user.save()
            return user
        except DjangoUnicodeDecodeError as e:
            return e


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('username', 'password')


class CSRFTokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ('token')
