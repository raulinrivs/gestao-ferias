from django.urls import path, include
from django.views.generic import TemplateView
from api.views import SolicitacaoViewSet, SetorViewSet, \
    ChangePasswordView, CreateUserViewSet, PasswordTokenCheckAPI, \
    ResetPasswordView, SetNewPasswordAPIView, UserViewSet, LoginAPIViewSet, \
    CSRFTokenAPIViewSet, LogoutAPIViewSet, SessionValidatorViewSet, \
    WhoAmIViewSet
from rest_framework import routers
from rest_framework.schemas import get_schema_view

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'user', CreateUserViewSet)
router.register(r'solicitacao', SolicitacaoViewSet)
router.register(r'setores', SetorViewSet)
# router.register(r'accounts', WhoAmIViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('csrf/', CSRFTokenAPIViewSet.as_view(), name='api-csrf'),
    path('accounts/login/', LoginAPIViewSet.as_view(), name='api-login'),
    path('accounts/logout/', LogoutAPIViewSet.as_view(), name='api-logout'),
    path('session/', SessionValidatorViewSet.as_view(), name='api-session'),
    path('whoami/', WhoAmIViewSet.as_view(), name='api-whoami'),
    path('accounts/password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('accounts/password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('accounts/password_reset_confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('accounts/password_reset_complete/', SetNewPasswordAPIView.as_view(), name='password_reset_complete'),
    path('api-auth/', include('rest_framework.urls',
                              namespace='rest_framework')),
    path('api_schema', get_schema_view(
        title='API Schema', description='Guide'), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'api_schema'}
    ), name='docs'),
]
