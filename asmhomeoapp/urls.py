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
    path('addpatient/', views.addpatient, name='addpatient'),
    path('delpatient/<str:regno>/', views.delpatient, name='delpatient'),
    path('adminpage2/', views.adminpage2, name='adminpage2'),
    path('allusers_data/', views.allusers_data, name='allusers_data'),
    path('search_section/', views.search_section, name='search_section'),
    path('sendsms/', views.sendsms, name='sendsms'),
    path('change_data/', views.change_data, name='change_data'),
    path('change_heroheading/', views.change_heroheading, name='change_heroheading'),
    path('change_heroheading/<str:stat>/', views.change_heroheading, name='change_heroheading'),
    path('change_clinictimings', views.change_clinictimings, name='change_clinictimings'),
    path('change_clinictimings/<str:stat>/', views.change_clinictimings, name='change_clinictimings'),
    path('change_aboutdata/<str:stat>/', views.change_aboutdata, name='change_aboutdata'),
    path('change_aboutdata/', views.change_aboutdata, name='change_aboutdata'),
    path('change_contactdata/', views.change_contactdata, name='change_contactdata'),
    path('read_messages/', views.read_messages, name='read_messages'),
    path('delmsg/<str:stat>/', views.delmsg, name='delmsg'),
]
