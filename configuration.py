import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

# Courses path's
COURSES_FIXTURE = PROJECT_ROOT/ 'courses/management/fixtures/courses_fixture.json'
LESSONS_FIXTURE = PROJECT_ROOT/ 'courses/management/fixtures/lessons_fixtures.json'

# Users path's
USES_FIXTURE = PROJECT_ROOT/ 'users/management/fixtures/users_fixture.json'
PAYMENTS_FIXTURE = PROJECT_ROOT/ 'users/management/fixtures/payments_fixture.json'

# Regexp's

VIDEO_LINK = re.compile(r'^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/.+$')