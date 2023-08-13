from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (TagViewSet, UserViewSet, IngredientViewSet,
                       RecipeViewSet, UserSubscriptionsViewSet,
                       UserSubscribeView)


router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'users', UserViewSet)
router.register(r'subscriptions', UserSubscriptionsViewSet,
                basename='subscriptions')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('users/<int:user_id>/subscribe/', UserSubscribeView.as_view())
]
