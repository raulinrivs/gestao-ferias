from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission
from django.contrib.auth.models import AbstractUser, BaseUserManager


class SetorManager(models.Manager):

    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Setor(models.Model):
    class Meta:
        verbose_name_plural = "Setores"

    name = models.CharField(_("name"), max_length=150, unique=True)
    contingente = models.IntegerField(blank=True, null=True)
    recursos_humanos = models.BooleanField(default=False)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    def __str__(self) -> str:
        return f'{self.name}'


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, matricula, password, **extra_fields):
        if not matricula:
            raise ValueError('The given matricula must be set')
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
    matricula = models.CharField(
        max_length=15, verbose_name='Matricula', unique=True)
    email = models.EmailField(unique=True)
    data_admissao = models.DateField(
        verbose_name='Data de admissão', default=timezone.now)
    gestor = models.BooleanField(verbose_name='Gestor', default=False)
    data_senha = models.DateField(
        verbose_name='Data da ultima troca de senha',
        default=timezone.now)
    setores = models.ManyToManyField(
        Setor,
        verbose_name=_("setores"),
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = []

    username = None

    objects = UserManager()


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
        verbose_name='Data de criação', default=timezone.now)

    def __str__(self) -> str:
        return f'{self.tipo_ferias} - {self.status} - {self.solicitante}'
