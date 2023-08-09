from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Tag, Recipe
from rest_framework import viewsets, filters
from api.filters import IngredientFilter
from api.serializers import IngredientSerializer, TagSerialiser, RecipeSerializer, RecipeCreateSerializer, UserSubscriptionsSerializer
from api.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from api.filters import RecipeFilter
from rest_framework.decorators import action
from users.models import User, Follow


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # Если хотим, чтобы доступ был только для авторизованных пользователей
    # используем IsAuthenticated, вместо AllowAny
    permission_classes = (AllowAny,)
    filter_backends = DjangoFilterBackend
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Информация о тегах."""
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = RecipeFilter
    search_fields = ['name', 'tags__name']
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer
        elif self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk=None):
        # Implement your logic for adding/removing a recipe from favorites here
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk=None):
        # Implement your logic for adding/removing a recipe from shopping cart here
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['patch'],
        permission_classes=[IsAuthenticated, ]
    )
    def update_recipe(self, request, pk=None):
        recipe = self.get_object()    
        # Проверяем, что текущий пользователь является автором рецепта
        if recipe.author != request.user:
            return Response(
                {"detail": "Недостаточно прав для выполнения операции"},
                status=status.HTTP_403_FORBIDDEN
            )     
        serializer = RecipeCreateSerializer(
            recipe,
            data=request.data,
            partial=True  # Разрешаем обновлять только указанные поля
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def delete_recipe(self, request, pk=None):
        recipe = self.get_object()

        # Проверяем, что текущий пользователь является автором рецепта
        if recipe.author != request.user:
            return Response(
                {"detail": "Недостаточно прав для выполнения операции"},
                status=status.HTTP_403_FORBIDDEN
            )
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSubscriptionsSerializer

    def get_queryset(self):
        return User.objects.filter(subscriptions__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        author = self.get_object()
        if author == request.user:
            return Response({"detail": "Нельзя подписываться на самого себя!"}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.get_or_create(user=request.user, author=author)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='subscribe')
    def unsubscribe(self, request, pk=None):
        author = self.get_object()
        Follow.objects.filter(user=request.user, author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





