import requests
from social_core.backends.oauth import BaseOAuth2

class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ''
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture')
    ]

    def authorization_url(self):
        """Return the authorization endpoint."""
        return "https://" + self.setting('DOMAIN') + "/authorize"

    def access_token_url(self):
        """Return the token endpoint."""
        return "https://" + self.setting('DOMAIN') + "/oauth/token"

    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']

    def get_user_details(self, response):
        print(response)  # Imprime la respuesta para ver qué contiene
        url = 'https://dev-1z63nyizcs7ivvpz.us.auth0.com/userinfo'  # URL de la API de UserInfo
        headers = {'Authorization': 'Bearer ' + response['access_token']}  # Usamos el token de acceso
        
        # Hacemos la solicitud GET a la API de UserInfo
        resp = requests.get(url, headers=headers)
        
        # Si la respuesta es exitosa (200 OK)
        if resp.status_code == 200:
            userinfo = resp.json()
            
            # Devolvemos los datos del usuario
            return {
                'username': userinfo.get('nickname', userinfo.get('name')),  # Usa 'name' si 'nickname' no está
                'first_name': userinfo.get('name'),  # Extraemos 'name' como nombre completo
                'picture': userinfo.get('picture'),  # Foto de perfil
                'user_id': userinfo.get('sub')  # ID del usuario en Auth0
            }
        else:
            # Si algo falla, puedes gestionar el error de la manera que prefieras
            raise Exception(f'Error al obtener detalles del usuario: {resp.status_code}, {resp.text}')
    
# Esta función está POR FUERA de la clase Auth0. Es una función independiente.
def getRole(request):
    user = request.user
    authUser = user.social_auth.filter(provider="auth0")[0]
    accessToken = authUser.extra_data['access_token']
    url = "https://dev-1z63nyizcs7ivvpz.us.auth0.com/userinfo"
    headers = {'authorization': 'Bearer ' + accessToken}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()
    role = userinfo['dev-1z63nyizcs7ivvpz.us.auth0.com/role']
    return role
