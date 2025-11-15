from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

    def validate(self, data):
        inn = data['inn']
        if not inn.isdigit():
            raise serializers.ValidationError('Некорректный ИНН!')
        if len(inn) < 10:
            raise serializers.ValidationError('Длина ИНН должна быть от 10 до 12 цифр!')
        return data