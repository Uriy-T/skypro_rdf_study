from django.contrib.auth.models import AbstractUser
from django.db import models
from courses.models import CourseModel, LessonModel


class MainUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Номер телефона'
    )
    city = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Город'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email} {self.username}'


class Payments(models.Model):
    class PaymentTypes(models.TextChoices):
        TRANSFER = 'transfer', 'перевод'
        CASH = 'cash', 'наличные'

    user = models.ForeignKey(
        MainUser,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )

    payed_course = models.ForeignKey(
        CourseModel,
        null=True,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name='Курс'
    )

    payed_lesson = models.ForeignKey(
        LessonModel,
        null=True,
        on_delete=models.SET_NULL,
        related_name='payments',
        verbose_name='Урок'
    )

    payed_sum = models.DecimalField(
        max_digits=2,
        decimal_places=...,
        null=False,
        blank=False,
        verbose_name='Сумма оплаты'
    )

    payment_type = models.CharField(
        max_length=25,
        null=False,
        choices=PaymentTypes.choices,
        default=PaymentTypes.TRANSFER,
        verbose_name='Тип оплаты'
    )

    def __str__(self):
        if self.payed_course:
            return f'{self.payed_course.course_title}: {self.payed_sum} - {self.payment_date}'
        elif self.payed_lesson:
            return f'{self.payed_lesson.lesson_title}: {self.payed_sum} - {self.payment_date}'

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-payment_date']
