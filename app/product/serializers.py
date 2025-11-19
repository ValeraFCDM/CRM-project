from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['quantity', 'created_at', 'updated_at']

    def validate(self, data):
        if data['purchase_price'] <= 0 or data['sale_price'] <= 0:
            raise serializers.ValidationError('Стоимость товара должна быть больше 0!')
        return data