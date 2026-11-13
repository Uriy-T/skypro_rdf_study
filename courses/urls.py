from django.urls import path
from courses.apps import CoursesConfig
from rest_framework.routers import DefaultRouter

from courses.views import (CoursesViewSet,
                           CreateLessonsAPIView,
                           ListLessonsAPIView,
                           SingleLessonAPIView,
                           UpdateLessonAPIView,
                           DeleteLessonAPIView)

app_name = CoursesConfig.name
router = DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='courses')

urlpatterns = [
                  path('lesson/create', CreateLessonsAPIView.as_view(), name='create_lesson'),
                  path('course/<int:pk>/lessons/list/', ListLessonsAPIView.as_view(), name='list_lesson'),
                  path('lesson/<int:pk>/', SingleLessonAPIView.as_view(), name='single_lesson'),
                  path('lesson/update/<int:pk>/', UpdateLessonAPIView.as_view(), name='update_lesson'),
                  path('lesson/delete/<int:pk>/', DeleteLessonAPIView.as_view(), name='delete_lesson'),

              ] + router.urls
