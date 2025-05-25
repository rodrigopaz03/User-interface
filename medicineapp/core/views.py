from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
import requests

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
        archivo = request.FILES.get('imagen')
        paciente_id = request.POST.get('paciente_id')
        if not paciente_id:
            message = 'Debes seleccionar un paciente'
        elif archivo:
            files = {
                'imagen': (archivo.name, archivo, archivo.content_type)
            }
            # Añadimos el paciente_id en el form data
            data = {'paciente_id': paciente_id}

            url = settings.SERVER1_URL  # Asegúrate de que termina con '/'
            try:
                response = requests.post(url, files=files, data=data)
                if response.status_code == 201:
                    message = 'Imagen subida con éxito al servidor'
                else:
                    message = f'Error: {response.status_code} - {response.text}'
            except Exception as e:
                message = f'Excepción al enviar: {e}'
        else:
            message = 'No se recibió ningún archivo'
    
    return render(request, 'core/upload.html', { 'message': message,'API_BASE': settings.SERVER2_URL})

@csrf_exempt  
def pacientes_menu(request):
    """
    Menú de opciones para gestión de pacientes e historias.
    """
    return render(request, 'core/pacientes.html', {
        'SERVER2_URL': settings.SERVER2_URL
    })

@csrf_exempt  
def paciente_nuevo(request):
    """
    Vista para registrar un nuevo paciente (y su historia inicial).
    """
    return render(request, 'core/paciente_crear.html', {
        'SERVER2_URL': settings.SERVER2_URL
    })

@csrf_exempt
def historia_consulta(request):
    """
    Página de consulta de historias clínicas (solo lectura).
    """
    return render(request, 'core/historias_consulta.html', {
        'API_BASE': settings.SERVER2_URL
    })

@csrf_exempt
def historia_actualizar(request):
    """
    Página para actualizar historias clínicas.
    """
    return render(request, 'core/historias_actualizar.html', {
        'API_BASE': settings.SERVER2_URL
    })
