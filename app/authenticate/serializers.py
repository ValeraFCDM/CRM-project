from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=50)
    password_confirm = serializers.CharField(write_only=True, min_length=8, max_length=50)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Пароли не совпадают!')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserAttachSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError('Пользователь не найден!')
        if user.company:
            raise serializers.ValidationError(f'Пользователь уже прикреплен к компании {user.company}!')
        data['user'] = user
        return data