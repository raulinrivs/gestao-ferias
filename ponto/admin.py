
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Solicitacao

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'matricula')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'gestor'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined', 'data_admissao')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Solicitacao)