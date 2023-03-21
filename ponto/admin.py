
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Solicitacao


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('matricula', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'gestor'
                )
        }),
        ('Important dates', {
            'fields': (
                'last_login', 'date_joined', 'data_admissao', 'data_senha')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('matricula', 'password1', 'password2'),
        }),
    )
    list_display = ('matricula', 'first_name', 'last_name', 'is_staff')
    search_fields = ('matricula', 'first_name', 'last_name')
    ordering = ('date_joined',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Solicitacao)
