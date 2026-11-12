from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from courses.models import CourseModel, LessonModel
from courses.serializers import CourseSerializer, LessonSerializer


class CoursesViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = CourseModel.objects.all()


class CreateLessonsAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = LessonModel.objects.all()


class ListLessonsAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('pk')
        return LessonModel.objects.filter(course_bind=course_id)


class SingleLessonAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = LessonModel.objects.all()


class UpdateLessonAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = LessonModel.objects.all()


class DeleteLessonAPIView(generics.DestroyAPIView):
    queryset = LessonModel.objects.all()
