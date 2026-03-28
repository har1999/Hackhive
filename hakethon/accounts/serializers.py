from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class LoginSerializer(serializers.Serializer):
    phone = serializers.RegexField(r'^\+?[0-9]{10,13}$', error_messages={'invalid': 'Enter a valid Indian phone number'})
    name = serializers.CharField(max_length=100, required=False, default='')
    role = serializers.ChoiceField(choices=['worker', 'contractor'], default='worker')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'name', 'role', 'is_verified', 'date_joined']
        read_only_fields = ['id', 'date_joined']
