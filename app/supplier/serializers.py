from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ['company']

    def validate(self, data):
        inn = data['inn']
        if not inn.isdigit():
            raise serializers.ValidationError('Некорректный ИНН!')
        if len(inn) < 10:
            raise serializers.ValidationError('Длина ИНН должна быть от 10 до 12 цифр!')

        if self.context:
            data['company'] = self.context['company']
        return data