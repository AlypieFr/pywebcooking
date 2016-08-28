from rest_framework import serializers
from main.models import Recipe
from main.controllers import CRecipe


class RecipeSerializer(serializers.Serializer):
    ingredients = serializers.ListField()
    equipment = serializers.ListField()
    instructions = serializers.ListField()
    proposals = serializers.ListField()
    categories = serializers.ListField()

    def create(self, validated_data):
        return CRecipe.add_new(**validated_data)

    def update(self, va):
        return True
