from rest_framework import serializers

from miapp.models import CiudadanoModel

class CiudadanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CiudadanoModel
        fields = '__all__'