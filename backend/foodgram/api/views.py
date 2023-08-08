from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient
from rest_framework import viewsets
from api.filters import IngredientFilter
from api.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # Если хотим, чтобы доступ был только для авторизованных пользователей
    # используем IsAuthenticated, вместо AllowAny
    permission_classes = AllowAny
    filter_backends = DjangoFilterBackend
    filterset_class = IngredientFilter
    pagination_class = None
