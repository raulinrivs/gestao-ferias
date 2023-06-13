from django.urls import path, include
from django.views.generic import TemplateView
from api.views import FirstLoginView, SolicitacaoViewSet, SetorViewSet, \
    ChangePasswordView, CreateUserViewSet, PasswordTokenCheckAPI, \
    ResetPasswordView, SetNewPasswordAPIView, UserViewSet, LoginAPIViewSet, \
    CSRFTokenAPIViewSet, LogoutAPIViewSet, SessionValidatorViewSet, \
    WhoAmIViewSet
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'create_user', CreateUserViewSet)
router.register(r'solicitacao', SolicitacaoViewSet)
router.register(r'setores', SetorViewSet)
# router.register(r'accounts', WhoAmIViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='API Sunset - Gestão de Férias',
        default_version='1.0.0',
        description='Documentação da API Sunset',
    ),
    public=True,
)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('csrf/', CSRFTokenAPIViewSet.as_view(), name='api-csrf'),
    path('accounts/login/', LoginAPIViewSet.as_view(), name='api-login'),
    path('accounts/logout/', LogoutAPIViewSet.as_view(), name='api-logout'),
    path('accounts/first_login/', FirstLoginView.as_view(), name='api-first-login'),
    path('session/', SessionValidatorViewSet.as_view(), name='api-session'),
    path('whoami/', WhoAmIViewSet.as_view(), name='api-whoami'),
    path('accounts/password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('accounts/password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', SetNewPasswordAPIView.as_view(), name='password_reset_complete'),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('api_schema', schema_view.with_ui('swagger', cache_timeout=0), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'api_schema'}
    ), name='docs'),
]
