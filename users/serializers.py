from rest_framework.serializers import ModelSerializer, SerializerMethodField

from users.models import MainUser, Payments


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UsersSerializer(ModelSerializer):
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
