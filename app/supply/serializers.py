from rest_framework import serializers
from .models import Supply

class SupplyProductQuantitySerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=1, write_only=True)
    quantity = serializers.IntegerField(min_value=1, max_value=100)

    def validate(self, data):
        storage = self.context['company'].storage
        product = storage.products.filter(id=data['id']).first()
        if not product:
            raise serializers.ValidationError(f'На складе не зарегистрирован товар с ID {data['id']}!')
        data['product'] = product
        del data['id']
        return data


class SupplySerializer(serializers.ModelSerializer):
    supplier_id = serializers.IntegerField(min_value=1, write_only=True)
    products = SupplyProductQuantitySerializer(many=True, write_only=True)

    class Meta:
        model = Supply
        fields = '__all__'
        read_only_fields = ['supplier']

    def validate(self, data):
        company = self.context['company']
        supplier = company.suppliers.filter(id=data['supplier_id']).first()
        if not supplier:
            raise serializers.ValidationError(f'Поставщик не зарегистрирован!')
        data['supplier'] = supplier
        del data['supplier_id']
        return data