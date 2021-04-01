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
from django.urls import path
import Concours.views

app_name = "Concours"

urlpatterns = [
    path('exams/', Concours.views.Home.as_view(), name='concours'),
    path('cart/', Concours.views.Cart.as_view(), name='cart'),
    path('pay/', Concours.views.Pay.as_view(), name='pay'),
    path('pack/', Concours.views.Pack.as_view(), name='pack'),
    path('service/', Concours.views.Service.as_view(), name='service'),
    path('receipt/<str:id>/', Concours.views.receipt, name='receipt'),
    path('exams/add/<str:uid>/', Concours.views.add, name='add concours'),
    path('exams/remove/<str:uid>/', Concours.views.remove, name='remove concours'),
]
