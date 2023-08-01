from django.contrib import admin
from django.conf import settings
from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # что будет отображаться в админке
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    # по каким полям можно искать
    search_fields = ('pk', 'username', 'email', 'first_name', 'last_name')
    # по каким полям можно фильтровать объекты
    list_filter = ('username', 'email')
    # меняем стандартное отображения пустых полей, по умолчанию оно '-'.
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
    empty_value_display = settings.EMPTY_VALUE
