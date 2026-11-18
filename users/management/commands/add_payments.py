from pathlib import Path
import json
from typing import Any
from  django.utils.dateparse import parse_datetime

from django.core.management.base import BaseCommand
from configuration import PAYMENTS_FIXTURE

from users.models import Payments


def fixture_reader(path_to_fixture: Path) -> dict[str: Any]:
    with open(path_to_fixture, 'r', encoding='utf-8') as fixture:
        records = json.load(fixture)
    return records


class Command(BaseCommand):
    help = 'Очищает таблицу courses_courses и заполняет стартовым набором тестовых данных'

    def handle(self, *args, **kwargs):
        Payments.objects.all().delete()

        payments_data = [payment['fields'] for payment in fixture_reader(PAYMENTS_FIXTURE)]

        for payment in payments_data:
            new_payment = Payments.objects.create(
                user_id=payment['user'],
                payed_course_id=payment.get('payed_course'),
                payed_lesson_id=payment.get('payed_lesson'),
                payed_sum=payment['payed_sum'],
                payment_type=payment['payment_type']
            )

            if payment.get('payment_date'):
                dt = parse_datetime(payment['payment_date'])
                Payments.objects.filter(pk=new_payment.pk).update(payment_date=dt)

            if new_payment.payed_course_id:
                self.stdout.write(self.style.SUCCESS(f'Оплата от {new_payment.payment_date} за курс "{new_payment.payed_course.course_title}" зарегистрирована.'))

            elif new_payment.payed_lesson_id:
                self.stdout.write(self.style.SUCCESS(f'Оплата от {new_payment.payment_date} за урок "{new_payment.payed_lesson.lesson_title}" зарегистрирована.'))
