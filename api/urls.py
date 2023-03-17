from django.urls import path, include
from django.views.generic import TemplateView
from api.views import UserViewSet, SetorViewSet, ChangePasswordView, CreateUserViewSet
from rest_framework import routers
from rest_framework.schemas import get_schema_view

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', CreateUserViewSet)
router.register(r'setores', SetorViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api_schema', get_schema_view(title='API Schema', description='Guide'), name='api_schema'),
    path('docs/', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'api_schema'}
    ), name='docs'),
    # path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    # path('rest_password/<str:encoded_pk>/<str:token>/', ChangePasswordView.as_view(), name='auth_reset_password'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
