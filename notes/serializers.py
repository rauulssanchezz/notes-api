from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Note
        fields = ['id','user', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']