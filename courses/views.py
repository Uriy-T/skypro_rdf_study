from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from courses.models import CourseModel, LessonModel
from courses.serializers import CourseSerializer, LessonSerializer
from users.permissions import StudyMaterialsPermission


# Courses CRUD
class CoursesViewSet(ModelViewSet):
    """
    CRUD операции для работы с курсами
    """
    serializer_class = CourseSerializer
    queryset = CourseModel.objects.all()
    permission_classes = [StudyMaterialsPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return CourseModel.objects.none()

        groups = user.groups.values_list('name', flat=True)

        if 'Модератор' in groups:
            return CourseModel.objects.all()
        if 'Преподаватель' in groups:
            return CourseModel.objects.filter(owner=user)
        return CourseModel.objects.none()


# Lessons CRUD
class CreateLessonsAPIView(generics.CreateAPIView):
    """
    Создание урока
    """
    serializer_class = LessonSerializer
    queryset = LessonModel.objects.all()
    permission_classes = [StudyMaterialsPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListLessonsAPIView(generics.ListAPIView):
    """
    Получение списка всех уроков с фильтрацией по курсу и по владельцу.
    """
    serializer_class = LessonSerializer
    permission_classes = [StudyMaterialsPermission]

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        queryset = LessonModel.objects.filter(course_bind=course_id)

        user = self.request.user
        if not user.is_authenticated:
            return queryset.none()

        groups = set(user.groups.values_list('name', flat=True))

        if 'Модератор' in groups:
            return queryset

        if 'Преподаватель' in groups:
            return queryset.filter(owner=user)

        return queryset.none()


class SingleLessonAPIView(generics.RetrieveAPIView):
    """
    Получение конкретного урока
    """
    serializer_class = LessonSerializer
    queryset = LessonModel.objects.all()
    permission_classes = [StudyMaterialsPermission]


class UpdateLessonAPIView(generics.UpdateAPIView):
    """
    Обновление конкретного урока
    """
    serializer_class = LessonSerializer
    queryset = LessonModel.objects.all()
    permission_classes = [StudyMaterialsPermission]


class DeleteLessonAPIView(generics.DestroyAPIView):
    """
    Удаление конкретного урока
    """
    queryset = LessonModel.objects.all()
    permission_classes = [StudyMaterialsPermission]
