from django.urls import path, include
from django.views.generic import TemplateView
from api.views import SolicitacaoViewSet, SetorViewSet, \
    ChangePasswordView, CreateUserViewSet, PasswordTokenCheckAPI, \
    ResetPasswordView, SetNewPasswordAPIView, UserViewSet
from rest_framework import routers
from rest_framework.schemas import get_schema_view

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', CreateUserViewSet)
router.register(r'setores', SetorViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    # path('solicitacao/', SolicitacaoViewSet.as_view(), name='solicitacao'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', SetNewPasswordAPIView.as_view(), name='password_reset_complete'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api_schema', get_schema_view(title='API Schema', description='Guide'), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'api_schema'}
    ), name='docs'),
]
