from pathlib import Path
import json
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection
from configuration import COURSES_FIXTURE

from courses.models import CourseModel


def fixture_reader(path_to_fixture: Path) -> dict[str: Any]:
    with open(path_to_fixture, 'r', encoding='utf-8') as fixture:
        records = json.load(fixture)
    return records


class Command(BaseCommand):
    help = 'Очищает таблицу courses_courses и заполняет стартовым набором тестовых данных'

    def handle(self, *args, **kwargs):
        CourseModel.objects.all().delete()

        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE courses_coursemodel RESTART IDENTITY CASCADE;")

        course_data = [course['fields'] for course in fixture_reader(COURSES_FIXTURE)]

        for course in course_data:
            new_course = CourseModel.objects.create(
                course_title=course['course_title'],
                course_preview=course.get('course_preview', ''),
                description=course.get('description', '')
            )

            self.stdout.write(self.style.SUCCESS(f'Курс "{new_course.course_title}" создан.'))
