from django.shortcuts import render
from django.conf import settings
import requests
def home(request):
    return render(request, 'main_app/home.html')

def server2(request):
    return render(request, 'main_app/server2.html')

def server3(request):
    return render(request, 'main_app/server3.html')

def server4(request):
    return render(request, 'main_app/server4.html')

def server5(request):
    return render(request, 'main_app/server5.html')

def server1_image(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if archivo:
            # Empaquetar el archivo en 'files' para enviar por requests
            files = {
                'archivo': (archivo.name, archivo.read(), archivo.content_type)
            }
            # URL del microservicio (server1)
            url = getattr(settings, 'SERVER1_URL', 'http://127.0.0.1:8001/server1/')
            
            # Enviamos el archivo por POST
            response = requests.post(url, files=files)
            
            if response.status_code == 201:
                return render(request, 'resultado.html', {'msg': 'Imagen guardada en server1 con éxito'})
            else:
                return render(request, 'resultado.html', {'msg': 'Error al guardar en server1'})
    return render(request, 'main_app/server1.html')

