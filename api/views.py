# Django Imports
from django.core.mail import send_mail
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login, logout
from django.utils.encoding import force_bytes, \
    smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# REST Framework Imports
from rest_framework import viewsets, generics, permissions, \
    authentication, mixins, status, views
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.schemas import get_schema_view
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
    # filterset_fields = ['status', 'solicitante']
    filterset_fields = {'status': ["in", "exact"],
                        'solicitante': ["in", "exact"],
                        }

    def get_queryset(self):
        user = self.request.user
        setores = user.setores.all()
        if len(setores) > 0:
            if setores.filter(recursos_humanos=True):
                return self.queryset
            elif user.gestor:
                return self.queryset.filter(solicitante__setores__in=setores)
            else:
                return self.queryset.filter(solicitante=user)
        else:
            raise PermissionError('Usuário não está vinculado a nenhum setor')
        

    def perform_create(self, serializer):
        tempo_servico = (
            datetime.combine(date.today(), time(0, 0)) -
            datetime.combine(self.request.user.data_admissao, time(0, 0))
        )
        user = self.request.user
        setores = user.setores.all()
        solicitacoes_user = Solicitacao.objects.filter(solicitante=user)
        ferias_concluidas = solicitacoes_user.count()
        tempo_servico_result = (tempo_servico.days - (ferias_concluidas * 365))

        # Validação de Solicitação em aberto
        if solicitacoes_user.filter(status__in=('CRI', 'VGE', 'DEF', 'USU')).exists():
            raise ValidationError('Você já possui uma solicitação em aberto')

        # Validação de Contingente
        for setor in setores:
            solicitacoes = solicitacoes_user.filter(
                solicitante__setores=setor,
                status__in=('DEF', 'USU')
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
        gestores = User.objects.filter(gestor=True, setores__in=setores)
        for gestor in gestores:
            recipient_list.append(gestor.email)
        send_mail(subject, message, email_from, recipient_list)
        return Response(solicitacao, status=status.HTTP_201_CREATED)


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ['get', 'patch', 'delete']
    serializer_class = UserSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, pk):
        return 'a'


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
            raise ValidationError(serializer.error_messages)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.check_password(
                serializer.validated_data['old_password']
            ):
                request.user.set_password(serializer.data.get("new_password"))
                request.user.data_senha = date.today()
                request.user.save()
                request.session.flush()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Senha atualizada com sucesso.',
                }
                return Response(response)
            else:
                raise ValidationError("Senha incorreta!")
        return ValidationError(serializer.error_messages)


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
                current_site = 'localhost:8080'
                absolute_url = f'http://{current_site}/accounts/' + \
                    f'password_reset_confirm/{smart_str(uidb64)}/{token}/'
                subject = 'Reset de senha'
                message = absolute_url
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list)
                return Response({
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Email encaminhado com sucesso.',
                })
            else:
                raise ValidationError('Usuário não existente.')
        else:
            raise ValidationError(serializer.error_messages)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = RestPasswordRequestSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_b64decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                message='Token inválido.'
                                )
            return Response({'uid64': uidb64, 'token': token}, 
                            status=status.HTTP_200_OK,
                            message='Token válido.')
        except DjangoUnicodeDecodeError as e:
            raise ValidationError(e)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        request.user.data_senha = date.today()
        request.user.save()
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
        matricula = request.data.get('matricula')
        password = request.data.get('password')
        if request.user.is_authenticated:
            return Response(
                {'detail': 'Voce já está logado'},
                status=status.HTTP_400_BAD_REQUEST)

        if matricula is None or password is None:
            return Response(
                {'detail': 'Favor inserir senha e matricula'},
                status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(matricula=matricula, password=password)

        if user is None:
            return Response({'detail': 'Credenciais inválidas'},
                            status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        return Response({'detail': 'Login realizado com sucesso'},
                        status=status.HTTP_200_OK)


class LogoutAPIViewSet(views.APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'detail': 'Você não está logado.'},
                            status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return Response({'detail': 'Usuário deslogado com sucesso.'},
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
