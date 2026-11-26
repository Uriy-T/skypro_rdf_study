from rest_framework import generics
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

from users.models import MainUser, Payments, Subscription
from users.serializers import (UsersRetrieveSerializer,
                               UsersCreateSerializer,
                               UsersUpdateSerializer,
                               PaymentsSerializer,
                               SubscriptionSerializer)


# Users CRUD________________
class CreateUserAPIView(generics.CreateAPIView):
    """
    Создание пользователя (регистрация).
    """

    serializer_class = UsersCreateSerializer
    queryset = MainUser.objects.all()
    permission_classes = [AllowAny]


class ListUserAPIView(generics.ListAPIView):
    """
    Получение списка всех имеющихся пользователей и их данных.
    """

    serializer_class = UsersRetrieveSerializer
    queryset = MainUser.objects.all()


class SingleUserAPIView(generics.RetrieveAPIView):
    """
    Получение данных о конкретном пользователе.
    """

    serializer_class = UsersRetrieveSerializer
    queryset = MainUser.objects.all()


class UpdateUserAPIView(generics.UpdateAPIView):
    """
    Обновление данных о конкретном пользователе.
    """

    serializer_class = UsersUpdateSerializer
    queryset = MainUser.objects.all()


class DeleteUserAPIView(generics.DestroyAPIView):
    """
    Удаление конкретного пользователя.
    """

    queryset = MainUser.objects.all()


# Payments CRUD ________________
class CreatePaymentAPIView(generics.CreateAPIView):
    """
    Регистрация платежа.
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class UserPaymentsListAPI(generics.ListAPIView):
    """
    Получение истории платежей
    - фильтруется по платежам за курс/урок курса и по типу средства платежа;
    - сортировка по дате платежа.
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('payed_course', 'payed_lesson', 'payment_type')
    ordering_fields = ('payment_date',)


class SinglePaymentsAPI(generics.RetrieveAPIView):
    """
    Получение данных о конкретном платеже.
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class UpdatePaymentAPIView(generics.UpdateAPIView):
    """
    Изменение данных о платеже.
    """

    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()


class DeletePaymentAPIView(generics.DestroyAPIView):
    """
    Удаление платежа.
    """

    queryset = Payments.objects.all()


# Subscription CRUD________________

class CreateSubscriptionAPIView(generics.CreateAPIView):
    """
    Установка подписки на курс
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteSubscriptionAPIView(generics.DestroyAPIView):
    """
    Снятие подписки на курс
    """
    queryset = Subscription.objects.all()

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
