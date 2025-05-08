import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import urlencode
from .auth0_helper import validate_token, get_or_create_user
from .decorators import login_required, role_required
import json

def index(request):
    return render(request, 'core/index.html')

@csrf_exempt
@login_required
def upload_image(request):
    if not request.session.get('user_payload'):
        return redirect('/login')
    
    message = ''
    if request.method == 'POST':
        archivo = request.FILES.get('imagen')
        if archivo:
            files = {'imagen': (archivo.name, archivo, archivo.content_type)}
            url = getattr(settings, 'SERVER1_URL')
            try:
                headers = {
                    'Authorization': f"Bearer {request.session.get('access_token')}"
                }
                response = requests.post(url, files=files, headers=headers)
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
@role_required('medico', 'enfermero')
def pacientes_menu(request):
    return render(request, 'core/pacientes.html', {
        'SERVER2_URL': settings.SERVER2_URL,
        'user_roles': request.session['user_payload'].get(f'https://{settings.AUTH0_DOMAIN}/roles', [])
    })

@csrf_exempt
@login_required
@role_required('medico', 'enfermero')
def paciente_nuevo(request):
    return render(request, 'core/paciente_crear.html', {
        'SERVER2_URL': settings.SERVER2_URL
    })

@csrf_exempt
@login_required
@role_required('medico')
def historial_form(request):
    return render(request, 'core/historias.html', {
        'SERVER2_URL': settings.SERVER2_URL
    })

# Auth0 Views
def login(request):
    query_params = urlencode({
        'response_type': 'code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
        'scope': settings.AUTH0_SCOPE,
        'audience': settings.AUTH0_AUDIENCE,
        'state': request.GET.get('next', '/'),
    })
    return redirect(f'https://{settings.AUTH0_DOMAIN}/authorize?{query_params}')

def callback(request):
    code = request.GET.get('code')
    if not code:
        return redirect('/login')
    token = "simulated_token"
    payload = {
        'sub': 'auth0|123456',
        'email': 'user@example.com',
        'name': 'Test User',
        f'https://{settings.AUTH0_DOMAIN}/roles': ['medico']  # Simulamos que es médico
    }
    
    request.session['user_payload'] = payload
    request.session['access_token'] = token
    
    next_url = request.GET.get('state', '/')
    return redirect(next_url)

def logout(request):
    request.session.flush()
    query_params = urlencode({
        'client_id': settings.AUTH0_CLIENT_ID,
        'returnTo': settings.LOGOUT_REDIRECT_URL,
    })
    return redirect(f'https://{settings.AUTH0_DOMAIN}/v2/logout?{query_params}')

def unauthorized(request):
    return render(request, 'core/unauthorized.html')