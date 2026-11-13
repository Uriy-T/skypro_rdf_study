from rest_framework import generics
from users.models import MainUser
from users.serializers import UsersSerializer


class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UsersSerializer
    queryset = MainUser.objects.all()

class ListUserAPIView(generics.ListAPIView):
    serializer_class = UsersSerializer


class SingleUserAPIView(generics.RetrieveAPIView):
    serializer_class = UsersSerializer
    queryset = MainUser.objects.all()


class UpdateUserAPIView(generics.UpdateAPIView):
    serializer_class = UsersSerializer
    queryset = MainUser.objects.all()


class DeleteUserAPIView(generics.DestroyAPIView):
    queryset = MainUser.objects.all()
