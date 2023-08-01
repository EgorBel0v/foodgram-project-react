from django.db import models
from users.models import User
from django.core.validators import MinValueValidator


class Ingredient(models.Model):
    """ Модель ингридиента, создаем ее первую, без нее
     нельзя создать модель рецепта. """
    name = models.CharField(
        max_length=100,
        verbose_name='Название ингредиента'
        )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения'
        )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """ модель Тегов."""
    name = models.CharField(
        max_length=100,
        verbose_name='Название тега'
        )
    color = models.CharField(
        max_length=15,
        verbose_name='Цвет тега'
        )
    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """ Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
        )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
        )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
        )
    description = models.TextField(
        verbose_name='Описание рецепта'
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
        )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)'
        )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
        )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """ Модель игридиентов в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Рецепт'

    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipeingredients',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1, 'Количество не менее 1'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorite(models.Model):
    """ Модель списка избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь, владелец списка избранного',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Список избранного'
        # Ограничение на модель, каждый рецепт может быть добавлен
        # в избранное только один раз, это избавит от дублей
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт "{self.recipe}" в списке избранного у '
            f'пользователя {self.user}'
        )


class ShoppingList(models.Model):
    """ Модель списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='Пользователь, владелец списка покупок'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_lists',
        verbose_name='Рецепт, добавленный в список покупок'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_lists'
            )
        ]

    def __str__(self):
        return (
            f'Рецепт "{self.recipe}" в списке покупок у '
            f'пользователя {self.user}'
        )
