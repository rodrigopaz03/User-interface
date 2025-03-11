"""
URL configuration for medical_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views
from django.urls import path
from .views import server1_image

urlpatterns = [
    path('', views.home, name='home'),         
    path('server1-imagen/', server1_image, name='server1_image'),
    path('server2/', views.server2, name='server2'),
    path('server3/', views.server3, name='server3'),
    path('server4/', views.server4, name='server4'),
    path('server5/', views.server5, name='server5'),
]
