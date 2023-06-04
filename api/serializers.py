from base64 import urlsafe_b64decode
import json
from django.forms import ValidationError
from django.core.mail import send_mail
from rest_framework import serializers
from datetime import datetime, date, time, timedelta
from config import settings
from ponto.models import CustomUser as User, Solicitacao, Setor
from api.validators import validador_ferias_integral, validador_ferias_venda, \
    validador_ferias_parcial
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError


class SetorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setor
        fields = ('id', 'name', 'contingente', 'recursos_humanos')


class UserSerializer(serializers.ModelSerializer):
    setores = SetorSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'


class UserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'matricula', 'data_admissao')


class CreateUserSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(allow_blank=True)

    class Meta:
        model = User
        fields = (
            'matricula', 'email', 'first_name', 'last_name', 'setores',
            'gestor', 'data_admissao'
        )


class FirstLoginSerializer(serializers.Serializer):
    matricula = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    class Meta:
        fields = ('matricula', 'email')

    def validate(self, attrs):
        user = User.objects.get(matricula=attrs['matricula'], email=attrs['email'])
        if user:
            if user.last_login is None:
                return super().validate(attrs)
            else:
                raise serializers.ValidationError(
                    "Usuário ja realizou o seu primeiro login."
                )
        raise serializers.ValidationError("Matricula e email não existentes.")


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


class SolicitacaoSerializer(serializers.ModelSerializer):
    solicitante = UserDashboardSerializer(many=False, read_only=True)

    class Meta:
        model = Solicitacao
        fields = '__all__'

    def update(self, instance, validated_data):
        request = self.context.get('request')

        instance.status = validated_data.get('status', instance.status)
        instance.data_criacao = validated_data.get('data_criacao', instance.data_criacao)
        instance.intervalos = validated_data.get('intervalos', instance.intervalos)
        instance.tipo_ferias = validated_data.get('tipo_ferias', instance.tipo_ferias)

        subject = 'Solicitação de ferias alterada'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.user.email]
        message = f'Solicitação : {instance}'

        # Envio de email para Gestor
        if instance.status == 'VGE' or instance.status == 'RGE':
            if request.user.gestor:
                users_rh = User.objects.filter(gestor=False, setores__recursos_humanos=True)
                for user in users_rh:
                    recipient_list.append(user.email)
            else:
                raise PermissionError('Voce não possui permissão para alterar a solicitação.')
        
        # Envio de email para RH
        elif instance.status == 'DEF' or instance.status == 'RRH':
            if request.user.setores.filter(recursos_humanos=True).exists():
                user_gestores = User.objects.filter(gestor=True, setores__in=instance.solicitante.setores.all())
                for user in user_gestores:
                    recipient_list.append(user.email)
            else:
                raise PermissionError('Voce não possui permissão para alterar a solicitação.')
        
        instance.save()

        send_mail(subject, message, email_from, recipient_list)
        return instance

    def validate(self, attrs):
        if self.instance:
            intervalos = json.loads(self.instance.intervalos)
            tipo_ferias = self.instance.tipo_ferias
            data_criacao = datetime.combine(self.instance.data_criacao, time(0, 0))
        else:
            intervalos = json.loads(attrs.get('intervalos'))
            tipo_ferias = attrs.get('tipo_ferias')
            data_criacao = datetime.combine(date.today(), time(0, 0))
        for chave, valor in intervalos.items():
            intervalos[chave] = datetime.strptime(valor, '%d/%m/%Y')

        if intervalos['data_inicial_1'] - data_criacao < timedelta(days=30):
            raise ValidationError('Só é possivel solicitar férias com data inicial daqui 30 dias')

        if tipo_ferias == 'INT':
            validador_ferias_integral(
                intervalos['data_inicial_1'], intervalos['data_final_1'])
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
        email = attrs.get('email')
        if User.objects.get(email=email):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError('Email não existente.')


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
    matricula = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('matricula', 'password')


class CSRFTokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ('token')
