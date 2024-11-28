from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(write_only=True)  # Add password as write-only

    def create(self, validated_data):
        # Pop the password from validated data
        password = validated_data.pop('password', None)
        # Create a user without the password set
        user = CustomUser.objects.create(**validated_data)
        if password:
            # Hash and set the password
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # Update instance with validated data
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            # Hash and set the password
            instance.set_password(password)
        instance.save()
        return instance
