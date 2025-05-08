from functools import wraps
from django.http import HttpResponseRedirect
from django.conf import settings
from .auth0_helper import validate_token

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_payload' not in request.session:
            return HttpResponseRedirect(f'/login?next={request.path}')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def role_required(*required_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if 'user_payload' not in request.session:
                return HttpResponseRedirect(f'/login?next={request.path}')
            
            user_roles = request.session['user_payload'].get(
                f'https://{settings.AUTH0_DOMAIN}/roles', []
            )
            
            if not any(role in required_roles for role in user_roles):
                return HttpResponseRedirect('/unauthorized/')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator