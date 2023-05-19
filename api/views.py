# Django Imports
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
# from django.urls import reverse
from django.utils.encoding import force_bytes, \
    smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# REST Framework Imports
from rest_framework import viewsets, generics, permissions, \
    authentication, mixins, status, views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError
# API app Imports
from api.serializers import CSRFTokenSerializer, FirstLoginSerializer, \
    UserSerializer, SolicitacaoSerializer, SetorSerializer, \
    ChangePasswordSerializer, RestPasswordRequestSerializer, \
    CreateUserSerializer, SetNewPasswordSerializer, LoginSerializer
from config import settings
# PONTO app Imports
from ponto.models import Setor, CustomUser as User, Solicitacao
# General Imports
from datetime import datetime, date, time
from random import choice
import string
from base64 import urlsafe_b64encode, urlsafe_b64decode
# from config import settings


class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = SolicitacaoSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        setores = user.setores.all()
        self.queryset.filter(solicitante=user)
        if setores:
            for setor in setores:
                if setor.recursos_humanos and user.gestor:
                    return super().get_queryset()
                elif setor.recursos_humanos:
                    return self.queryset.exclude(solicitante=user)
                elif user.gestor:
                    return self.queryset.filter(solicitante__setores=setor)
                else:
                    return self.queryset.filter(solicitante=user)
        else:
            raise Exception("Usuário não está vinculado a nenhum setor")
        return super().get_queryset()

    def perform_create(self, serializer):
        tempo_servico = (
            datetime.combine(date.today(), time(0, 0)) -
            datetime.combine(self.request.user.data_admissao, time(0, 0))
        )
        user = self.request.user
        setores = user.setores.all()
        ferias_concluidas = self.queryset.filter(status='CON', solicitante=user).count()
        tempo_servico_result = (tempo_servico.days - (ferias_concluidas * 365))

        # Validação de Solicitação em aberto
        if self.queryset.filter(
            solicitante=user, status__in=['CRI', 'VGE', 'DEF']
        ).exists():
            raise ValidationError('Você já possui uma solicitação em aberto')

        # Validação de Contingente
        for setor in setores:
            solicitacoes = self.queryset.filter(
                solicitante__setores=setor,
                status='DEF'
            )
            if solicitacoes.count() >= setor.contingente:
                raise ValidationError('O contingente do setor já foi atingido, ' +
                                      'entre em contato com a gestão')

        # Validação de tempo de serviço suficiente
        if tempo_servico_result < 365:
            raise ValidationError('Você ainda não possui tempo de serviço para' +
                                  'solicitar férias')

        # Validação de férias vencidas
        if tempo_servico_result > 700:
            raise ValidationError('Você possui férias vencidas, favor entrar em ' +
                                  'contato com o seu Gestor ou RH')

        solicitacao = Solicitacao.objects.create(
            status='CRI',
            tipo_ferias=serializer.validated_data['tipo_ferias'],
            intervalos=serializer.validated_data['intervalos'],
            solicitante=self.request.user,
        )
        subject = 'Solicitação de ferias criada'
        message = f'Solicitação : {solicitacao}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.request.user.email]
        send_mail(subject, message, email_from, recipient_list)
        return Response(solicitacao, status=status.HTTP_201_CREATED)


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    authentication_classes = [authentication.BaseAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = UserSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


def password_generator():
    senha = ''
    for i in range(8):
        senha += choice(string.ascii_letters + string.digits)
    return senha


class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def perform_create(self, serializer):
        senha = password_generator()
        validated_data = serializer.validated_data
        if validated_data.get('matricula'):
            matricula = validated_data.get('matricula')
        else:
            matricula = User.objects.last()
            matricula = matricula.id + 1
        user = User.objects.create_user(
            matricula=matricula,
            password=senha,
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            gestor=validated_data.get('gestor'),
            data_admissao=validated_data.get('data_admissao')
        )
        for setor in validated_data.get('setores'):
            setor.user_set.add(user)
        return Response(user, status=status.HTTP_201_CREATED)


class FirstLoginView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = FirstLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(
                matricula=serializer.validated_data['matricula'],
                email=serializer.validated_data['email']
            )
            senha = password_generator()
            user.set_password(senha)
            user.save()
            subject = 'Informações de Login'
            message = f'Matricula: {user.matricula}\nSenha: {senha}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [serializer.validated_data['email']]
            send_mail(subject, message, email_from, recipient_list)
            return Response(
                'Email encaminhado para o usuário.',
                status=status.HTTP_200_OK
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if self.request.user.check_password(
                serializer.validated_data['old_password']
            ):
                self.request.user.set_password(serializer.data.get("new_password"))
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = RestPasswordRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            user = User.objects.get(email=email)
            if user:
                uidb64 = urlsafe_b64encode(force_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                relative_link = reverse(
                    'password_reset_confirm',
                    kwargs={'uidb64': smart_str(uidb64), 'token': token})
                current_site = get_current_site(request=request).domain
                absolute_url = f'http://{current_site}{relative_link}'
                subject = 'Reset de senha'
                message = absolute_url
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list)
                return Response(status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = RestPasswordRequestSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_b64decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'uid64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            print(e)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class CSRFTokenAPIViewSet(generics.GenericAPIView):
    serializer_class = CSRFTokenSerializer

    def get(self, request):
        response = Response(data={'X-CSRFToken': get_token(request)},
                            status=status.HTTP_200_OK)
        return response


class LoginAPIViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if request.user.is_authenticated:
            return Response(
                {'detail': 'Voce já está logado'},
                status=status.HTTP_400_BAD_REQUEST)

        if username is None or password is None:
            return Response(
                {'detail': 'Favor inserir senha e matricula'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'detail': 'Credenciais inválidas'},
                            status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({'detail': 'Login realizado com sucesso'},
                        status=status.HTTP_200_OK)


class LogoutAPIViewSet(views.APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'You\'re not logged in.'},
                            status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return Response({'detail': 'Successfully logged out.'},
                        status=status.HTTP_200_OK)


class SessionValidatorViewSet(views.APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'isAuthenticated': False})

        return Response({'isAuthenticated': True})


class WhoAmIViewSet(views.APIView):
    serializer_class = UserSerializer

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'isAuthenticated': False},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = self.serializer_class(User.objects.get(id=request.user.id))
        return Response(user.data, status=status.HTTP_200_OK)
