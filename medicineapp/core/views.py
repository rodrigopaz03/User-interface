import requests
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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
                'imagen': (archivo.name, archivo.read(), archivo.content_type),
            }
            url = getattr(settings, 'SERVER1_URL', 'http://10.128.0.8:8080/upload/')
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
