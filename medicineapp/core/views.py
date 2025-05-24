from django.http import HttpResponse
import requests
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from medicineapp.auth0backend import getRole
from django.contrib.auth.decorators import login_required

@csrf_exempt  
def index(request):
    """
    Página principal con tema hospitalario y botón para ir al servidor de exámenes.
    """
    return render(request, 'core/index.html')

@csrf_exempt  
def upload_image(request):
    message = ''
    if request.method == 'POST':
        # Se obtiene el archivo del formulario
        archivo = request.FILES.get('imagen')
        if archivo:
            # Preparamos la petición POST para enviar el archivo al microservicio
            files = {
  'imagen': (archivo.name, archivo, archivo.content_type)  # sin .read()
}
            url = getattr(settings, 'SERVER1_URL')
            try:
                response = requests.post(url, files=files)
                if response.status_code == 201:
                    message = 'Imagen subida con éxito al servidor'
                else:
                    message = f'Error: {response.status_code} - {response.text}'
            except Exception as e:
                message = f'Excepción al enviar: {e}'
        else:
            message = 'No se recibió ningún archivo'
    return render(request, 'core/upload.html', {'message': message})

@csrf_exempt  
@login_required
def pacientes_menu(request):
    """
    Menú de opciones para gestión de pacientes e historias.
    """
    role = getRole(request)
    if role == "medico" or role == "enfermera":
        return render(request, 'core/pacientes.html', {
            'SERVER2_URL': settings.SERVER2_URL
        })
    else:
        return HttpResponse("Unauthorized User")

@csrf_exempt  
def paciente_nuevo(request):
    """
    Vista para registrar un nuevo paciente (y su historia inicial).
    """
    role = getRole(request)
    if role == "medico" or role == "enfermera":
        return render(request, 'core/paciente_crear.html', {
            'SERVER2_URL': settings.SERVER2_URL
        })
    else:
        return HttpResponse("Unauthorized User")

@login_required
@csrf_exempt
def historia_consulta(request):
    role = getRole(request)
    if role not in ('medico','enfermera'):
        return HttpResponse("Unauthorized", status=403)

    # Solo renderizamos la plantilla; el JS la llenará vía GET
    return render(request, 'core/historias_consulta.html', {
        'API_BASE': settings.SERVER2_URL
    })

@login_required
@csrf_exempt
def historia_actualizar(request):
    role = getRole(request)
    if role not in ('medico','enfermera'):
        return HttpResponse("Unauthorized", status=403)

    return render(request, 'core/historias_actualizar.html', {
        'API_BASE': settings.SERVER2_URL
    })