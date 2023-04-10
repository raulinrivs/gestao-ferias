
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser, Solicitacao, Setor


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
                'setores', 'user_permissions', 'gestor'
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
    list_filter = ("is_staff", "is_superuser", "is_active", "setores")
    search_fields = ('matricula', 'first_name', 'last_name')
    ordering = ('date_joined',)
    filter_horizontal = (
        "setores",
        "user_permissions",
    )


class SetorAdmin(admin.ModelAdmin):
    filter_horizontal = (
        "permissions",
    )

admin.site.unregister(Group)
admin.site.register(Setor, SetorAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Solicitacao)
