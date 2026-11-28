from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import MainUser
from courses.models import LessonModel


class LessonsCreateTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Подготавливаем нужные элементы окружения:
        - Создаем группу;
        - Назначаем группе права;
        - Создаем пользователя;
        - Назначаем пользователю группу.
        """
        cls.tutor_group = Group.objects.create(name='Преподаватель')

        lessons_content_type = ContentType.objects.get_for_model(LessonModel)

        permissions = Permission.objects.filter(
            content_type=lessons_content_type,
            codename__in=['add_lessonmodel', 'change_lessonmodel', 'delete_lessonmodel', 'view_lessonmodel']
        )
        cls.tutor_group.permissions.set(permissions)

        cls.tutor_user = MainUser.objects.create_user(
            username='tutor_test',
            email='tutor@example.com',
            password='password123'
        )

        cls.tutor_user.groups.add(cls.tutor_group)

    def setUp(self):
        """
        - Авторизуем пользователя перед исполнением теста;
        - Заготавливаем изображение для поля предпросмотра.
        - Создаем курс для прикрепления уроков.
        """

        # Превью для курса
        with open(r'E:\My_WorkShops\Dev_WorkShop\previews\blender.jpg', 'rb') as img:
            self.course_preview = SimpleUploadedFile(
                'Just_test_course_image.jpg',
                content=img.read(),
                content_type='image/jpeg')

        # Превью для урока 1
        with open(r'E:\1872.jpg', 'rb') as img:
            self.lesson1_preview = SimpleUploadedFile(
                'Just_test_image.jpg',
                content=img.read(),
                content_type='image/jpeg')

        # Превью для урока 2
        with open(r'E:\1872.jpg', 'rb') as img:
            self.lesson2_preview = SimpleUploadedFile(
                'Just_test_image.jpg',
                content=img.read(),
                content_type='image/jpeg')

        self.client.force_authenticate(self.tutor_user)

        # Создаем курс для привязки
        data_for_course = {
            'course_title': 'Процедурное моделирование Blender с помощью системы Geometry Nodes.',
            'course_preview': self.course_preview,
            'description': 'Создавайте свои управляемые ассеты на основе нод геометрии в Blender 3D'
        }

        blender_course = self.client.post(
            '/courses/',
            data=data_for_course
        )

        self.assertEqual(blender_course.status_code, status.HTTP_201_CREATED)
        self.course_id = blender_course.data['id']

    def test_create_lessons(self):
        """Тест создания урока"""

        data_for_lesson1 = {
            'lesson_title': 'Основные ноды',
            'lesson_preview': self.lesson1_preview,
            'description': 'Создаем простую геометрию',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response = self.client.post(
            '/lesson/create/',
            data=data_for_lesson1
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['lesson_title'], 'Основные ноды')
        self.assertTrue('lessons/previews/' in response.data['lesson_preview'])
        self.assertEqual(response.data['description'], 'Создаем простую геометрию')
        self.assertEqual(response.data['video_link'], 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/')
        self.assertEqual(response.data['course_bind'], 1)

    def test_get_lessons_list(self):
        """Тест получение списка уроков курса"""

        # Создаем урок 1
        data_for_lesson1 = {
            'lesson_title': 'Основные ноды',
            'lesson_preview': self.lesson1_preview,
            'description': 'Создаем простую геометрию',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response_lesson1 = self.client.post(
            '/lesson/create/',
            data=data_for_lesson1
        )

        self.assertEqual(response_lesson1.status_code, status.HTTP_201_CREATED)

        # Создаем урок 2
        data_for_lesson2 = {
            'lesson_title': 'Компонентные меши',
            'lesson_preview': self.lesson2_preview,
            'description': 'Создаем геометрию, состоящую из нескольких меш-объектов',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response_lesson2 = self.client.post(
            '/lesson/create/',
            data=data_for_lesson2
        )

        self.assertEqual(response_lesson2.status_code, status.HTTP_201_CREATED)

        # Тестируем получение списка уроков с пагинацией.
        lessons_list = self.client.get(
            f'/course/{self.course_id}/lessons/list/'
        )

        self.assertEqual(lessons_list.status_code, status.HTTP_200_OK)
        self.assertEqual(lessons_list.data['count'], 2)
        self.assertEqual(lessons_list.data['next'], None)
        self.assertEqual(lessons_list.data['previous'], None)
        self.assertIsInstance(lessons_list.data['results'], list)
        self.assertEqual(len(lessons_list.data['results']), 2)

        lesson_1 = next(
            item for item in lessons_list.data['results']
            if item['lesson_title'] == 'Основные ноды'
        )

        self.assertEqual(lesson_1['description'],
                         'Создаем простую геометрию'
                         )
        self.assertTrue('lessons/previews/' in lesson_1['lesson_preview'])

        self.assertEqual(lesson_1['video_link'], 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/')
        self.assertEqual(lesson_1['course_bind'], self.course_id)
        self.assertEqual(lesson_1['owner'], self.tutor_user.id)

        lesson_2 = next(
            item for item in lessons_list.data['results']
            if item['lesson_title'] == 'Компонентные меши'
        )

        self.assertTrue('lessons/previews/' in lesson_2['lesson_preview'])
        self.assertEqual(
            lesson_2['description'],
            'Создаем геометрию, состоящую из нескольких меш-объектов'
        )
        self.assertEqual(lesson_2['video_link'], 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/')
        self.assertEqual(lesson_2['course_bind'], self.course_id)
        self.assertEqual(lesson_2['owner'], self.tutor_user.id)

    def test_get_single_lesson(self):
        """Тест получения одного урока"""

        # Создаем урок
        data_for_lesson = {
            'lesson_title': 'Основные ноды',
            'lesson_preview': self.lesson1_preview,
            'description': 'Создаем простую геометрию',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response_lesson = self.client.post(
            '/lesson/create/',
            data=data_for_lesson
        )

        self.assertEqual(response_lesson.status_code, status.HTTP_201_CREATED)

        lesson_id = response_lesson.data['id']

        get_lesson = self.client.get(f'/lesson/{lesson_id}/')

        self.assertEqual(get_lesson.status_code, status.HTTP_200_OK)

    def test_update_lesson(self):
        """Тест изменения урока курса"""

        # Создаем урок
        data_for_lesson = {
            'lesson_title': 'Основные ноды',
            'lesson_preview': self.lesson1_preview,
            'description': 'Создаем простую геометрию',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response_lesson = self.client.post(
            '/lesson/create/',
            data=data_for_lesson
        )

        self.assertEqual(response_lesson.status_code, status.HTTP_201_CREATED)
        lesson_id = response_lesson.data['id']

        # Изменяем урок

        data_for_update = {
            'lesson_title': 'Основные ноды геометрии',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7gy1/',
            'description': 'Создаем простую геометрию и учимся ее изменять'
        }

        update_response = self.client.patch(f'/lesson/update/{lesson_id}/',
                                            data=data_for_update)

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['lesson_title'], 'Основные ноды геометрии')
        self.assertEqual(update_response.data['description'], 'Создаем простую геометрию и учимся ее изменять')
        self.assertEqual(update_response.data['video_link'],
                         'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7gy1/')

    def test_delete_lesson(self):
        """Тест удаления урока"""

        # Создаем урок
        data_for_lesson = {
            'lesson_title': 'Основные ноды',
            'lesson_preview': self.lesson1_preview,
            'description': 'Создаем простую геометрию',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response_lesson = self.client.post(
            '/lesson/create/',
            data=data_for_lesson
        )

        self.assertEqual(response_lesson.status_code, status.HTTP_201_CREATED)
        lesson_id = response_lesson.data['id']

        # Удаляем урок

        deleted_lesson = self.client.delete(
            f'/lesson/delete/{lesson_id}/'
        )

        self.assertEqual(deleted_lesson.status_code, status.HTTP_204_NO_CONTENT)

        # Дополнительная проверка удаления

        get_lesson = self.client.get(f'/lesson/{lesson_id}/')

        self.assertEqual(get_lesson.status_code, status.HTTP_404_NOT_FOUND)


class LessonsOtherRolesTest(APITestCase):
    """Набор тестов под другими ролями"""

    @classmethod
    def setUpTestData(cls):
        """
        Подготавливаем нужные элементы окружения:
        - Создаем группу;
        - Назначаем группе права;
        - Создаем пользователя;
        - Назначаем пользователю группу.
        """
        cls.tutor_group = Group.objects.create(name='Преподаватель')
        cls.moderator_group = Group.objects.create(name='Модератор')

        lessons_content_type = ContentType.objects.get_for_model(LessonModel)

        tutor_permissions = Permission.objects.filter(
            content_type=lessons_content_type,
            codename__in=['add_lessonmodel', 'change_lessonmodel', 'delete_lessonmodel', 'view_lessonmodel']
        )
        cls.tutor_group.permissions.set(tutor_permissions)

        moderator_permissions = Permission.objects.filter(
            content_type=lessons_content_type,
            codename__in=['change_lessonmodel', 'view_lessonmodel']
        )

        cls.moderator_group.permissions.set(moderator_permissions)

        cls.tutor_user_1 = MainUser.objects.create_user(
            username='tutor1_test',
            email='tutor1@example.com',
            password='password123'
        )

        cls.tutor_user_1.groups.add(cls.tutor_group)

        cls.tutor_user_2 = MainUser.objects.create_user(
            username='tutor2_test',
            email='tutor2@example.com',
            password='password1234'
        )

        cls.tutor_user_2.groups.add(cls.tutor_group)

        cls.moderator_user = MainUser.objects.create_user(
            username='moderator_test',
            email='moderator@example.com',
            password='password12345')

        cls.moderator_user.groups.add(cls.moderator_group)

    def setUp(self):
        """
        - Авторизуем пользователя перед исполнением теста;
        - Заготавливаем изображение для поля предпросмотра.
        - Создаем курс для прикрепления уроков.
        """

        # Превью для курса
        with open(r'E:\My_WorkShops\Dev_WorkShop\previews\blender.jpg', 'rb') as img:
            self.course_preview = SimpleUploadedFile(
                'Just_test_course_image.jpg',
                content=img.read(),
                content_type='image/jpeg')

        # Превью для урока 1
        with open(r'E:\1872.jpg', 'rb') as img:
            self.lesson1_preview = SimpleUploadedFile(
                'Just_test_image.jpg',
                content=img.read(),
                content_type='image/jpeg')

        # Превью для урока 2
        with open(r'E:\1872.jpg', 'rb') as img:
            self.lesson2_preview = SimpleUploadedFile(
                'Just_test_image.jpg',
                content=img.read(),
                content_type='image/jpeg')

        self.client.force_authenticate(self.tutor_user_1)

        # Создаем курс для привязки
        data_for_course = {
            'course_title': 'Процедурное моделирование Blender с помощью системы Geometry Nodes.',
            'course_preview': self.course_preview,
            'description': 'Создавайте свои управляемые ассеты на основе нод геометрии в Blender 3D'
        }

        blender_course = self.client.post(
            '/courses/',
            data=data_for_course
        )

        self.assertEqual(blender_course.status_code, status.HTTP_201_CREATED)
        self.course_id = blender_course.data['id']

    def test_actions_by_moderator(self):
        """Проверяем CRUD операции для модератора"""

        # Создаем урок от имени преподавателя

        data_for_lesson = {
            'lesson_title': 'Основные ноды',
            'lesson_preview': self.lesson1_preview,
            'description': 'Создаем простую геометрию',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response_lesson = self.client.post(
            '/lesson/create/',
            data=data_for_lesson
        )

        self.assertEqual(response_lesson.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_lesson.data['lesson_title'], 'Основные ноды')
        self.assertTrue('lessons/previews/' in response_lesson.data['lesson_preview'])
        self.assertEqual(response_lesson.data['description'], 'Создаем простую геометрию')
        self.assertEqual(response_lesson.data['video_link'],
                         'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/')
        self.assertEqual(response_lesson.data['course_bind'], self.course_id)

        lesson_id = response_lesson.data['id']

        # Авторизуемся под ролью модератора
        self.client.force_authenticate(self.moderator_user)

        # Получаем созданный урок
        get_lesson = self.client.get(f'/lesson/{lesson_id}/')

        self.assertEqual(get_lesson.status_code, status.HTTP_200_OK)
        self.assertEqual(response_lesson.data['lesson_title'], 'Основные ноды')
        self.assertTrue('lessons/previews/' in response_lesson.data['lesson_preview'])
        self.assertEqual(response_lesson.data['description'], 'Создаем простую геометрию')
        self.assertEqual(response_lesson.data['video_link'],
                         'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/')
        self.assertEqual(response_lesson.data['course_bind'], self.course_id)

        # Изменяем созданный урок
        data_for_update = {
            'lesson_title': 'Основные ноды геометрии',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7gy1/',
            'description': 'Создаем простую геометрию и учимся ее изменять'
        }

        update_response = self.client.patch(f'/lesson/update/{lesson_id}/',
                                            data=data_for_update)

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['lesson_title'], 'Основные ноды геометрии')
        self.assertEqual(update_response.data['description'], 'Создаем простую геометрию и учимся ее изменять')
        self.assertEqual(update_response.data['video_link'],
                         'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7gy1/')

        # Удаляем созданный урок
        deleted_lesson = self.client.delete(
            f'/lesson/delete/{lesson_id}/'
        )

        self.assertEqual(deleted_lesson.status_code, status.HTTP_403_FORBIDDEN)

    def test_actions_by_another_tutor(self):
        """Проверяем CRUD операции для преподавателя, который не является автором урока"""

        # Создаем урок от имени первого преподавателя

        data_for_lesson = {
            'lesson_title': 'Основные ноды',
            'lesson_preview': self.lesson1_preview,
            'description': 'Создаем простую геометрию',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/',
            'course_bind': self.course_id
        }

        response_lesson = self.client.post(
            '/lesson/create/',
            data=data_for_lesson
        )

        self.assertEqual(response_lesson.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_lesson.data['lesson_title'], 'Основные ноды')
        self.assertTrue('lessons/previews/' in response_lesson.data['lesson_preview'])
        self.assertEqual(response_lesson.data['description'], 'Создаем простую геометрию')
        self.assertEqual(response_lesson.data['video_link'],
                         'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7ba2/')
        self.assertEqual(response_lesson.data['course_bind'], self.course_id)

        lesson_id = response_lesson.data['id']

        # Авторизуемся под ролью второго преподавателя
        self.client.force_authenticate(self.tutor_user_2)

        # Получаем созданный урок
        get_lesson = self.client.get(f'/lesson/{lesson_id}/')

        self.assertEqual(get_lesson.status_code, status.HTTP_403_FORBIDDEN)

        # Изменяем созданный урок
        data_for_update = {
            'lesson_title': 'Основные ноды геометрии',
            'video_link': 'https://youtube.com/video/2300d0f75272f3c84b7b622280ce7gy1/',
            'description': 'Создаем простую геометрию и учимся ее изменять'
        }

        update_response = self.client.patch(f'/lesson/update/{lesson_id}/',
                                            data=data_for_update)

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)

        # Удаляем созданный урок
        deleted_lesson = self.client.delete(
            f'/lesson/delete/{lesson_id}/'
        )

        self.assertEqual(deleted_lesson.status_code, status.HTTP_403_FORBIDDEN)
