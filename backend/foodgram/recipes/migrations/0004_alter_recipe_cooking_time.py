# Generated by Django 4.2.3 on 2023-10-25 14:55

from django.db import migrations, models
import recipes.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rename_description_recipe_text_alter_tag_color_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[recipes.models.validate_positive], verbose_name='Время приготовления (в минутах)'),
        ),
    ]
