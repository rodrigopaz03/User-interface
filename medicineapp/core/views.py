from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
import requests
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

@csrf_exempt  
def index(request):
    """
    Página principal con tema hospitalario y botón para ir al servidor de exámenes.
    """
    return render(request, 'core/index.html')

import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings

@csrf_exempt
def upload_image(request):
    message = ''
    if request.method == 'POST':
        archivo     = request.FILES.get('imagen')
        paciente_id = request.POST.get('paciente_id')

        if not paciente_id:
            message = 'Debes seleccionar un paciente'

        elif archivo:
            
            contenido = archivo.read()
            b64       = base64.b64encode(contenido).decode('ascii')

            CHUNK_SIZE = 200_000
            chunks     = [b64[i:i+CHUNK_SIZE] for i in range(0, len(b64), CHUNK_SIZE)]

            init_payload = {
                "paciente_id":  paciente_id,
                "filename":     archivo.name,
                "content_type": archivo.content_type,
                "chunks_count": len(chunks)
            }
            try:
                init_res = requests.post(
                    f"{settings.SERVER1_URL.rstrip('/')}/init-upload/",
                    json=init_payload
                )
                init_res.raise_for_status()
            except Exception as e:
                message = f'Error en init-upload: {e}'
                return render(request, 'core/upload.html', {
                    'message':    message,
                    'API_BASE':   settings.SERVER2_URL,
                    'API_UPLOAD': settings.SERVER1_URL.rstrip('/') + '/',
                })

            doc_id = init_res.json().get("doc_id")
            
            upload_url = f"{settings.SERVER1_URL.rstrip('/')}/upload-chunk/"
            tasks      = [
                {"doc_id": doc_id, "chunk_index": idx, "data": data}
                for idx, data in enumerate(chunks)
            ]
            errors = []
            with ThreadPoolExecutor(max_workers=min(8, len(tasks))) as executor:
                futures = {
                    executor.submit(requests.post, upload_url, json=payload): payload["chunk_index"]
                    for payload in tasks
                }
                for future in as_completed(futures):
                    idx = futures[future]
                    try:
                        resp = future.result()
                        resp.raise_for_status()
                    except Exception as e:
                        errors.append(f"chunk {idx}: {e}")

            if errors:
                message = "Errores enviando chunks: " + "; ".join(errors)
            else:
                message = "Imagen subida correctamente"

        else:
            message = 'No se recibió ningún archivo'

    return render(request, 'core/upload.html', {
        'message':    message,
        'API_BASE':   settings.SERVER2_URL,
        'API_UPLOAD': settings.SERVER1_URL.rstrip('/') + '/',
    })


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

@csrf_exempt
def combined_view(request):
    """
    Página combinada con Historia Clínica, Imágenes y Diagnóstico.
    """
    return render(request, 'core/combined.html', {
        'API_BASE':   settings.SERVER2_URL,                                  # microservicio de historias
        'API_UPLOAD': settings.SERVER1_URL.rstrip('/') + '/',                # microservicio de imágenes
        'API_DIAG':   settings.SERVER3_URL.rstrip('/') + '/'                 # microservicio de diagnósticos
    })


