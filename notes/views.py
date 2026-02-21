from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Note
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .serializers import NoteSerializer

class NoteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner()]

        return [IsAuthenticated()]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at', 'title']