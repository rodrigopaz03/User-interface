from django.urls import path
from .views import (
    index, upload_image, pacientes_menu, paciente_nuevo, 
    historial_form, login, callback, logout, unauthorized
)

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_image, name='upload_image'),
    path('pacientes/', pacientes_menu, name='pacientes_menu'),
    path('pacientes/nuevo/', paciente_nuevo, name='paciente_nuevo'),
    path('pacientes/historial/', historial_form, name='historial_form'),
    path('pacientes/consultar/', historial_form, name='pacientes_consultar'),
    path('pacientes/actualizar/', historial_form, name='pacientes_actualizar'),
    
    # Auth0 URLs
    path('login/', login, name='login'),
    path('callback/', callback, name='callback'),
    path('logout/', logout, name='logout'),
    path('unauthorized/', unauthorized, name='unauthorized'),
]