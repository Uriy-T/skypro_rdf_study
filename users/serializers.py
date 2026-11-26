from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from users.models import MainUser, Payments, Subscription


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


class SubscriptionSerializer(ModelSerializer):
    """
    Сериализатор объектов подписки на курсы
    """

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course']
        read_only_fields = ['user']

    def validate(self, attrs):
        user = self.context['request'].user
        course = attrs.get('course')

        if Subscription.objects.filter(user=user, course=course).exists():
            raise ValidationError(
                {"course": "Вы уже подписаны на этот курс."}
            )

        return attrs
