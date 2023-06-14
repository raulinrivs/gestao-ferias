"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# from ponto import views, urls
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', views.RegisterView.as_view()),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    # path('solicitacao/nova', views.SolicitacaoView.as_view(), name='solicitacao'),
    # path('solicitacao/<int:pk>/', views.SolicitacaoDetailView.as_view(), name='solicitacao_detail'),
    # path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('accounts/password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/v1/', include('api.urls'))
]
