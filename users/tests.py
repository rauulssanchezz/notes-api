from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.conf import settings

class UserApiTests(APITestCase):

    def setUp(self):
        self.android_header = {'HTTP_X_ANDROID_ID': settings.SECRET_KEY_ANDROID_ID}
        self.client.credentials(**self.android_header)
        # Creamos un usuario en la base de datos de pruebas (que está limpia)
        self.user = User.objects.create_user(username='raul', password='password123')
        # Creamos un token para este usuario manualmente para poder usarlo luego
        self.token = Token.objects.create(user=self.user)
        # Guardamos la URL usando reverse para no escribirla a mano
        self.profile_url = reverse('profile')

    def test_register(self):
        url = reverse('register')
        data = {'username': 'nuevo', 'email': 'n@e.com', 'password': '123'}
        # Enviamos el POST
        response = self.client.post(url, data)
        # Comprobamos: ¿Ha respondido 201 Created?
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_own_profile(self):
        # Ponemos el token en la cabecera
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            **self.android_header
        )
        response = self.client.get(self.profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Comprobamos directamente el campo que queremos:
        self.assertEqual(response.data['username'], 'raul')

    def test_logout_works(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key,
            **self.android_header
        )
        self.client.post(reverse('logout'))
        
        # Intentamos buscar el token en la DB. Si se ha borrado, .exists() será False.
        token_existe = Token.objects.filter(key=self.token.key).exists()
        self.assertFalse(token_existe)