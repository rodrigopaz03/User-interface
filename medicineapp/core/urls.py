"""
URL configuration for medicineapp project.

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
from django.urls import path
from .views import index, upload_image, pacientes_menu, paciente_nuevo, historial_form

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_image, name='upload_image'),
     # Menú de pacientes
    path('pacientes/',                     pacientes_menu,   name='pacientes_menu'),
    # Alta de paciente (con historia automática)
    path('pacientes/nuevo/',               paciente_nuevo,   name='paciente_nuevo'),
    # Consulta de historia clínica
    path('pacientes/consultar/',           historial_form,   name='pacientes_consultar'),
    # Actualización de la misma historia
    path('pacientes/actualizar/',          historial_form,   name='pacientes_actualizar'),
]


