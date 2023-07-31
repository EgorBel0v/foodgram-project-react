from djoser.serializers import UserCreateSerializer
from users.models import User


class UserSignUpSerializer(UserCreateSerializer):
    """Регистрации пользователей."""
    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password')
