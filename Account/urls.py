"""APOS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
import Account.views
from django.contrib.auth.views import *

urlpatterns = [

    path('auth/<str:email>/<str:password>/', Account.views.auth_login, name='auth login'),

    path('login/', LoginView.as_view(), name='login'),
    path('profile/', LoginView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('accounts/', include('django_registration.backends.activation.urls'), name='activate'),

    path('accounts/reset/', Account.views.PasswordResetViewer.as_view(), name='password_reset'),
    path('accounts/reset/done/', Account.views.PasswordResetDoneViewer.as_view(), name='password_reset_done'),

    path('accounts/signup/', Account.views.RegistrationViewer.as_view(), name='register'),
    path('registration/done/', Account.views.reg_done, name='register_done'),
    path('registration/fail/', Account.views.reg_fail, name='register_fail'),
    path('email/', Account.views.check_email, name='email'),

    path('reset/<uidb64>/<token>/', Account.views.PasswordResetConfirmViewer.as_view(), name='password_reset_confirm'),
    path('reset/done/', Account.views.PasswordResetCompleteViewer.as_view(), name='password_reset_complete'),

]
