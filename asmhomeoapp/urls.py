"""
URL configuration for asmhomeo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from asmhomeoapp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('loginpage/', views.loginpage, name='loginpage'),
    path('logoutpage/', views.logoutpage, name='logoutpage'),
    path('searchdata/', views.searchdata, name='searchdata'), 
    path('changestatus/', views.changestatus, name='changestatus'),   
    path('changestatus/<str:stat>/', views.changestatus, name='changestatus'),
    path('updatenotice', views.updatenotice, name='updatenotice'),
    path('updatenotice/<str:stat>/', views.updatenotice, name='updatenotice'),
    path('sendmessage/', views.sendmessage, name='sendmessage'),
]
