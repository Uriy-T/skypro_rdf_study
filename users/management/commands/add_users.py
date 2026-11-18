from pathlib import Path
import json
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection
from configuration import USES_FIXTURE
from users.models import MainUser


def fixture_reader(path_to_fixture: Path) -> dict[str: Any]:
    with open(path_to_fixture, 'r', encoding='utf-8') as fixture:
        records = json.load(fixture)
    return records


class Command(BaseCommand):
    help = 'Очищает таблицу courses_courses и заполняет стартовым набором тестовых данных'

    def handle(self, *args, **kwargs):
        MainUser.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE users_mainuser RESTART IDENTITY CASCADE;")

        users_data = [user['fields'] for user in fixture_reader(USES_FIXTURE)]

        for user in users_data:
            new_user = MainUser.objects.create(
                username=user['username'],
                password=user.get('password', ''),
                email=user.get('email', '')
            )

            self.stdout.write(self.style.SUCCESS(f'Пользователь "{new_user.username}" создан.'))
