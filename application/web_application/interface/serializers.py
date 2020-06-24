from rest_framework import serializers

from interface.models import CityData, CategoryData

class CityDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityData
        fields = '__all__'

class CategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryData
        fields = '__all__'