from rest_framework import serializers
from .models import User, Cliente

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'birth_date', 'password', 'is_staff', 'is_active']

    def create(self, validated_data):
        validated_data['user_type'] = 'cliente' 
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        Cliente.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
