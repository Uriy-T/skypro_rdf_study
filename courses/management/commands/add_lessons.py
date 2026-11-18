from pathlib import Path
import json
from typing import Any

from django.core.management.base import BaseCommand
from configuration import LESSONS_FIXTURE

from courses.models import LessonModel


def fixture_reader(path_to_fixture: Path) -> dict[str: Any]:
    with open(path_to_fixture, 'r', encoding='utf-8') as fixture:
        records = json.load(fixture)
    return records


class Command(BaseCommand):
    help = 'Очищает таблицу courses_lessonmodel и заполняет стартовым набором тестовых данных'

    def handle(self, *args, **kwargs):
        LessonModel.objects.all().delete()

        lessons_data = [lesson['fields'] for lesson in fixture_reader(LESSONS_FIXTURE)]

        for lesson in lessons_data:
            new_lesson = LessonModel.objects.create(
                lesson_title=lesson['lesson_title'],
                description=lesson.get('description', ''),
                lesson_preview=lesson.get('lesson_preview', ''),
                video_link = lesson['video_link'],
                course_bind_id= lesson['course_bind']
            )

            self.stdout.write(self.style.SUCCESS(f'Урок "{new_lesson.lesson_title}" создан.'))
