from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio']

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError('Email is not valid.')
        return value
