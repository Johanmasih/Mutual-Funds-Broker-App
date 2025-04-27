from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import EmailValidator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    
    def validate(self, data):
        # Ensure passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Validate email format using Django's built-in EmailValidator
        email_validator = EmailValidator()
        try:
            email_validator(data['email'])
        except DjangoValidationError:
            raise serializers.ValidationError("Invalid email format.")

        # Ensure username is unique
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("email already exists")
        
        # Validate strong password
        if not any(char.isdigit() for char in data['password1']) or not any(char.isalpha() for char in data['password1']):
            raise serializers.ValidationError("Password must contain both letters and numbers.")
        
        return data

    def create(self, validated_data):
        # Use password1 to create the user after validation
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username', ""),
            password=validated_data['password1']
        )
        return user