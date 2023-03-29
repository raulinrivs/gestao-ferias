from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, matricula, password, **extra_fields):
        if not matricula:
            raise ValueError('The given matricula must be set')
        matricula = matricula.lower()
        user = self.model(matricula=matricula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, matricula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(matricula, password, **extra_fields)

    def create_superuser(self, matricula, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(matricula, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    matricula = models.CharField(
        max_length=15, verbose_name='Matricula', unique=True)
    data_admissao = models.DateField(
        verbose_name='Data de admissão', default=now())
    gestor = models.ManyToManyField(Group, blank=True)
    data_senha = models.DateField(
        verbose_name='Data da ultima troca de senha',
        default=now())

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = []

    objects = UserManager()

# class CustomUserManager(UserManager):
#         def create_user(self, username: str, matricula: Optional[str] = ..., password: Optional[str] = ..., **extra_fields: Any) -> _T: # noqa: E501
#                 return super().create_user(username, matricula, password, **extra_fields) # noqa: E501


class Solicitacao(models.Model):
    class Meta:
        verbose_name_plural = "Solicitações"

    TIPO_FERIAS = [
                ('INT', 'Integral'),
                ('VEN', 'Venda'),
                ('PAR', 'Parcial'),
        ]
    STATUS = [
                ('CRI', 'Criada'),
                ('VGE', 'Validada pelo Gestor'),
                ('RGE', 'Recusada pelo Gestor'),
                ('DEF', 'Deferido'),
                ('RRH', 'Recusada pelo RH'),
                ('CON', 'Concluida'),
    ]
    status = models.CharField(choices=STATUS, max_length=3)
    tipo_ferias = models.CharField(choices=TIPO_FERIAS, max_length=3)
    intervalos = models.TextField()
    solicitante = models.ForeignKey(
                CustomUser, on_delete=models.DO_NOTHING)
    data_criacao = models.DateField(
        verbose_name='Data de criação', default=now())

    def __str__(self) -> str:
        return f'{self.tipo_ferias} - {self.status} - {self.solicitante}'
