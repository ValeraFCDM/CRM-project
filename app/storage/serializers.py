from rest_framework import serializers
from .models import Storage

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ['address']

    def validate(self, data):
        if self.context:
            data['company'] = self.context['company']
        return data

