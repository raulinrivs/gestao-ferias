from base64 import urlsafe_b64decode
from rest_framework import serializers
from ponto.models import CustomUser as User, Solicitacao, Group as Setor
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'matricula', 'data_admissao')



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

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
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


class RestPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ('email')

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            user = User.objects.filter(email=email).first()
        except:
            print('deu ruim')
        return super().validate(attrs)


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
