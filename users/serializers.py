from os import write

from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer

from users.models import MainUser, Payments


class PaymentsSerializer(ModelSerializer):
    """
    Сериализатор объектов платежей
    """

    class Meta:
        model = Payments
        fields = '__all__'


class UsersCreateSerializer(ModelSerializer):
    """
    Сериализатор созданния пользователя
    """

    class Meta:
        model = MainUser
        fields = ['id',
                  'email',
                  'password',
                  'phone_number',
                  'city',
                  'avatar',
                  'last_login',
                  'is_superuser',
                  'username',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'is_active',
                  'date_joined',
                  'groups',
                  'user_permissions'
                  ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        return make_password(value)


class UsersRetrieveSerializer(ModelSerializer):
    """
    Сериализатор получения пользователя/ей.
    """
    payments_history = PaymentsSerializer(many=True, read_only=True, source='payments')

    class Meta:
        model = MainUser
        fields = ['id',
                  'email',
                  'phone_number',
                  'city',
                  'avatar',
                  'last_login',
                  'is_superuser',
                  'username',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'is_active',
                  'date_joined',
                  'groups',
                  'user_permissions',
                  'payments_history'
                  ]


class UsersUpdateSerializer(ModelSerializer):
    """
    Сериализатор обновления пользователя
    """

    class Meta:
        model = MainUser
        fields = ['id',
                  'email',
                  'password',
                  'phone_number',
                  'city',
                  'avatar',
                  'last_login',
                  'is_superuser',
                  'username',
                  'first_name',
                  'last_name',
                  'is_staff',
                  'is_active',
                  'date_joined',
                  'groups',
                  'user_permissions'
                  ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        return make_password(value)

