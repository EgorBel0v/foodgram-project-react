from rest_framework import serializers
from recipes.models import (Tag, Ingredient, Recipe, RecipeIngredient,
                            Favorite, ShoppingList)
from users.models import User, Follow
from djoser.serializers import UserCreateSerializer, UserSerializer
from api.utils import Base64ImageField
from django.shortcuts import get_object_or_404
from django.db import transaction


def create_ingredients(ingredients, recipe):
    """Функция для создании/редактировании рецепта."""
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(Ingredient,
                                               id=ingredient.get('id'))
        amount = ingredient.get('amount')
        ingredient_list.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=amount
            )
        )
    RecipeIngredient.objects.bulk_create(ingredient_list)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class UserGetSerializer(UserSerializer):
    """Информация о пользователях."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return (request.user.is_authenticated
                and Follow.objects.filter(
                    user=request.user, author=obj
                ).exists())


class UserSignUpSerializer(UserCreateSerializer):
    """Регистрация пользователей."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
        # Делаем поля обязательными, т.к. используем DJOSER
        # И в settings прописываем
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с ингредиентами."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации об ингредиентах.
    Используется при работе с рецептами.
    """
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Создание рецептов."""
    tags = serializers.ListField(child=serializers.IntegerField())
    ingredients = serializers.ListField(child=serializers.DictField())

    class Meta:
        model = Recipe
        fields = ('name', 'image', 'text', 'cooking_time',
                  'ingredients', 'tags')

    image = Base64ImageField()

    @transaction.atomic
    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')

        # Create the recipe
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)

        # Create RecipeIngredient instances
        ingredient_list = []
        for ingredient in ingredients_data:
            current_ingredient = get_object_or_404(Ingredient, id=ingredient.get('id'))
            amount = ingredient.get('amount')
            ingredient_list.append(
                RecipeIngredient(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=amount
                )
            )
        RecipeIngredient.objects.bulk_create(ingredient_list)

        return recipe


class RecipeGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о рецепте."""
    tags = TagSerializer(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(many=True, read_only=True,
                                             source='recipeingredients')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Favorite.objects.filter(
                    user=request.user, recipe=obj
                ).exists())

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and ShoppingList.objects.filter(
                    user=request.user, recipe=obj
                ).exists())

# from djoser.serializers import UserCreateSerializer, UserSerializer
# from rest_framework import serializers
# from users.models import User, Follow
# from recipes.models import Ingredient, Tag, Recipe


# class UserInfoSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name',
#                   'last_name', 'is_subscribed')

#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         return (request.user.is_authenticated
#                 and Follow.objects.filter(
#                     user=request.user, author=obj
#                 ).exists())


# # class UserSignUpSerializer(UserCreateSerializer):
# #     """Регистрации пользователей."""
# #     class Meta:
# #         model = User
# #         fields = ('id', 'email', 'username',
# #                   'first_name', 'last_name', 'password')


# class IngredientSerializer(serializers.ModelSerializer):
#     """Сериализатор для ингредиентов."""
#     class Meta:
#         model = Ingredient
#         fields = '__all__'


# class TagSerialiser(serializers.ModelSerializer):
#     """Сериализатор для работы с тегами."""
#     class Meta:
#         model = Tag
#         fields = '__all__'


# # class UserGetSerializer(UserSerializer):
# #     """Сериализатор для работы с информацией о пользователях."""
# #     is_subscribed = serializers.SerializerMethodField()

# #     class Meta:
# #         model = User
# #         fields = ('email', 'id', 'username', 'first_name',
# #                   'last_name', 'is_subscribed')

# #     def get_is_subscribed(self, obj):
# #         request = self.context.get('request')
# #         return (request.user.is_authenticated
# #                 and Follow.objects.filter(
# #                     user=request.user, author=obj
# #                 ).exists())


# class RecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = (
#             'id', 'tags', 'ingredients', 'image', 'name', 'description',
#             'cooking_time',
#         )


# class RecipeCreateSerializer(serializers.ModelSerializer):
#     ingredients = IngredientSerializer(many=True)
#     tags = serializers.PrimaryKeyRelatedField(
#         queryset=Tag.objects.all(),
#         many=True
#     )
#     image = serializers.ImageField()

#     class Meta:
#         model = Recipe
#         fields = (
#             'ingredients', 'tags', 'image', 'name',
#             'description', 'cooking_time')


# class UserSubscriptionsSerializer(serializers.ModelSerializer):
#     is_subscribed = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ('email', 'id', 'username', 'first_name',
#                   'last_name', 'is_subscribed')

#     def get_is_subscribed(self, obj):
#         request = self.context.get('request')
#         return (request.user.is_authenticated
#                 and Follow.objects.filter(
#                     user=request.user, author=obj
#                 ).exists())
