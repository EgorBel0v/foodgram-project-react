from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from users.models import User
from recipes.models import Ingredient


class UserSignUpSerializer(UserCreateSerializer):
    """Регистрации пользователей."""
    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'
