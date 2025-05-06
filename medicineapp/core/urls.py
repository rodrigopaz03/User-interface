# core/urls.py

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PacienteViewSet,
    HistoriaClinicaViewSet,
    index,
    upload_image,
    pacientes_menu,
    paciente_nuevo,
    historial_form,
)

# 1) Configuramos el router de la API
router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='paciente')
router.register(r'historias', HistoriaClinicaViewSet, basename='historia')

# 2) Construimos urlpatterns combinando:
urlpatterns = [
    # — Primero todas las rutas generadas por el router (/api/... si lo incluyes así en tu project urls)
    *router.urls,

    # — Luego tus vistas de UI
    path('',                     index,             name='index'),
    path('upload/',              upload_image,      name='upload_image'),
    path('pacientes/',           pacientes_menu,    name='pacientes_menu'),
    path('pacientes/nuevo/',     paciente_nuevo,    name='paciente_nuevo'),
    path('pacientes/consultar/', historial_form,    name='pacientes_consultar'),
    path('pacientes/actualizar/',historial_form,    name='pacientes_actualizar'),
]


