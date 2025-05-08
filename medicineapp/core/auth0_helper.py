import json
from urllib.request import urlopen
from jose import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

def get_jwks():
    jsonurl = urlopen(f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json")
    return json.loads(jsonurl.read())

def validate_token(token):
    jwks = get_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        return None
    
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=settings.AUTH0_AUDIENCE,
                issuer=f"https://{settings.AUTH0_DOMAIN}/"
            )
            return payload
        except jwt.JWTError:
            return None
    return None

def get_or_create_user(payload):
    auth0_id = payload.get('sub')
    email = payload.get('email')
    name = payload.get('name', '')
    roles = payload.get(f'https://{settings.AUTH0_DOMAIN}/roles', [])
    
    try:
        user = User.objects.get(auth0_id=auth0_id)
    except ObjectDoesNotExist:
        user = User.objects.create(
            username=email,
            email=email,
            first_name=name,
            auth0_id=auth0_id,
            roles=roles
        )
    
    if user.roles != roles:
        user.roles = roles
        user.save()
    
    return user