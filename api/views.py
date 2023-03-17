#Django Imports
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.contrib.auth.models import UserManager
#REST Framework Imports
from rest_framework import viewsets, generics, permissions, authentication, mixins
#API app Imports
from api.serializers import UserSerializer, SolicitacaoSerializer, SetorSerializer, ChangePasswordSerializer, EmailSerializer, CreateUserSerializer
#PONTO app Imports
from ponto.models import Group as Setor, CustomUser as User, Solicitacao
#General Imports
from random import choice
import string
from base64 import urlsafe_b64encode


class SetorViewSet(viewsets.ModelViewSet):
    queryset = Setor.objects.all()
    serializer_class = SetorSerializer
    http_method_names = ['get']
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        senha = ''
        for i in range(8):
            senha += choice(string.ascii_letters + string.digits)
        print(senha)
        return super().create(request, *args, **kwargs)

class CreateUserViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        senha = password_generator()
        print(senha)
        user = User.objects.create_user(
            username=validated_data.get('matricula'),
            matricula=validated_data.get('matricula'),
            password=senha,
            email=validated_data.get('email'),
        )
        return user
    
def password_generator():
    senha = ''
    for i in range(8):
        senha += choice(string.ascii_letters + string.digits)
    return senha
    

# Criação de usuário certa...
# class CreateUserViewSet(mixins.CreateModelMixin,
#                         viewsets.GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = CreateUserSerializer
    
#     def perform_create(self, serializer):
#         senha = password_generator()
#         validated_data = serializer.validated_data
#         username = validated_data.get('first_name').lower() + '.' + validated_data.get('last_name').lower(),
#         user = User.objects.create_user(
#             username=username,
#             password=senha,
#             email=validated_data.get('email'),
#             first_name=validated_data.get('first_name'),
#             last_name=validated_data.get('last_name'),
#         )
#         for group in validated_data.get('groups'):
#             group.user_set.add(user)
#         return user


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = permissions.IsAuthenticated
    serializer_class = ChangePasswordSerializer


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_b64encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
    
    
class SolicitacaoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)