from rest_framework import serializers

from users.models import MainUser


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainUser
        fields = '__all__'
