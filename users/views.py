from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.models import MainUser, Payments
from users.serializers import UsersSerializer, PaymentsSerializer


# Users CRUD________________
class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UsersSerializer
    queryset = MainUser.objects.all()


class ListUserAPIView(generics.ListAPIView):
    serializer_class = UsersSerializer
    queryset = MainUser.objects.all()


class SingleUserAPIView(generics.RetrieveAPIView):
    serializer_class = UsersSerializer
    queryset = MainUser.objects.all()


class UpdateUserAPIView(generics.UpdateAPIView):
    serializer_class = UsersSerializer
    queryset = MainUser.objects.all()


class DeleteUserAPIView(generics.DestroyAPIView):
    queryset = MainUser.objects.all()


# Payments CRUD ________________
class CreatePaymentAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class UserPaymentsListAPI(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payed_course', 'payed_lesson', 'payment_type')
    ordering_fields = ('payment_date',)


class SinglePaymentsAPI(generics.RetrieveAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class UpdatePaymentAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class DeletePaymentAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
