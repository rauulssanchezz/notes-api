from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'username': {
                'error_messages': {
                    'required': 'El nombre de usuario es obligatorio.',
                    'invalid': 'Introduce un correo electrónico válido.'
                }
            },
            'email': {
                'error_messages': {
                    'required': 'El email es obligatorio.',
                    'unique': 'Este correo electrónico ya está en uso.',
                    'invalid': 'Introduce un correo electrónico válido.'
                }
            }
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)