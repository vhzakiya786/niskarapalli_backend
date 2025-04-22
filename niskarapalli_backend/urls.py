"""
URL configuration for niskarapalli_backend project.

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

from user_app.views import Login
from home_app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('home_app.urls')),
    path('login/',Login.as_view(),name='login'),

    path('home', views.user_create_update, name='user_create_update'),
    path('get_users/', views.get_users, name='get_users'),
    path('get_upi_ids/', views.get_upi_ids, name='get_upi_ids'),
    path('check_user_by_upi/', views.check_user_by_upi, name='check_user_by_upi'),
]
