from django.contrib import admin
from .models import MainUser, Payments


@admin.register(MainUser)
class UsersAdm(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    search_fields = ('username', 'email')


@admin.register(Payments)
class PaymentsAdm(admin.ModelAdmin):
    list_display = ('id', 'user', 'payed_course', 'payed_lesson', 'payment_date', 'payment_type')
    list_filter = ('user', 'payed_course', 'payed_lesson', 'payment_date', 'payment_type')
    search_fields = ('user', 'payed_course', 'payed_lesson', 'payment_date', 'payment_type')