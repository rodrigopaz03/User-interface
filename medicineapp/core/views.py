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
        archivo = request.FILES.get('imagen')
        if archivo:
            chunk_size = 1024 * 1024  # 1MB
            file_size = archivo.size
            total_chunks = (file_size + chunk_size - 1) // chunk_size  # redondeo hacia arriba

            imagen_id = None  # Se usará para enviar el ID en los chunks siguientes
            chunk_index = 0

            # Iteramos sobre cada chunk del archivo
            for chunk in archivo.chunks(chunk_size):
                data = {
                    'chunk_index': str(chunk_index),
                    'total_chunks': str(total_chunks),
                }
                # En el primer chunk, enviamos título y content_type
                if chunk_index == 0:
                    data['titulo'] = archivo.name
                    data['content_type'] = archivo.content_type
                else:
                    # En los siguientes, enviamos el id de la imagen creada previamente
                    data['imagen_id'] = imagen_id

                files = {
                    'imagen': (archivo.name, chunk, archivo.content_type),
                }
                url = getattr(settings, 'SERVER1_URL', 'http://10.128.0.14:8000/upload_chunk/')
                try:
                    response = requests.post(url, data=data, files=files)
                except Exception as e:
                    message = f'Excepción al enviar chunk {chunk_index}: {e}'
                    break

                if response.status_code == 201:
                    # En la primera petición se espera recibir el imagen_id
                    if chunk_index == 0:
                        imagen_id = response.json().get('imagen_id')
                        if not imagen_id:
                            message = 'No se recibió imagen_id en la respuesta del primer chunk'
                            break
                else:
                    message = f'Error en el chunk {chunk_index}: {response.status_code} - {response.text}'
                    break

                chunk_index += 1

            else:
                # Si se completaron todos los chunks sin errores:
                message = 'Imagen subida con éxito al servidor'
        else:
            message = 'No se recibió ningún archivo'
    return render(request, 'core/upload.html', {'message': message})
