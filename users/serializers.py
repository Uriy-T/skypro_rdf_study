from rest_framework import serializers

from users.models import MainUser, Payments


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainUser
        fields = '__all__'

class PaymentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payments
        fields= '__all__'
