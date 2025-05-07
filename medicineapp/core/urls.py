# core/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    index,
    upload_image,
    pacientes_menu,
    paciente_nuevo,
    historial_form,
)

urlpatterns = [
    path('',                    index,            name='index'),
    path('upload/',             upload_image,     name='upload_image'),
    path('pacientes/',          pacientes_menu,   name='pacientes_menu'),
    path('pacientes/nuevo/',    paciente_nuevo,   name='paciente_nuevo'),
    path('pacientes/historial/',historial_form,   name='historial_form'),
]


