from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Note

class NoteAPITests(APITestCase):

    def setUp(self):
        # Creamos dos usuarios para probar que uno no puede ver lo del otro
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        
        # Creamos una nota para el usuario 1
        self.note = Note.objects.create(
            user=self.user1, 
            title="Nota de User 1", 
            content="Contenido secreto"
        )
        
        self.url_list = reverse('notes-list') # Esto genera '/api/notes/'
        self.url_detail = reverse('notes-detail', kwargs={'pk': self.note.id})

    def test_create_note_authenticated(self):
        """Verificar que un usuario logueado puede crear una nota"""
        self.client.force_authenticate(user=self.user1)
        data = {'title': 'Nueva Nota', 'content': 'Bla bla'}
        response = self.client.post(self.url_list, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        # Verificamos que se asignó al usuario correcto automáticamente
        self.assertEqual(Note.objects.latest('id').user, self.user1)

    def test_list_notes_only_owner(self):
        """Verificar que un usuario solo ve SUS propias notas"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # User 2 no debería ver la nota de User 1
        self.assertEqual(len(response.data), 0)

    def test_update_note_is_owner(self):
        """Verificar que el permiso IsOwner funciona"""
        # User 2 intenta editar la nota de User 1
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Hackeado'}
        response = self.client.patch(self.url_detail, data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note_is_owner(self):
        """Verificar que el dueño sí puede borrar su nota"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)
