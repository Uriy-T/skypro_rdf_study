from django.contrib import admin
from .models import CourseModel, LessonModel

@admin.register(CourseModel)
class CourseAdm(admin.ModelAdmin):
    list_display = ('id', 'course_title')
    search_fields = ('course_title',)


@admin.register(LessonModel)
class ProductAdm(admin.ModelAdmin):
    list_display = ('id', 'lesson_title', 'course_bind')
    list_filter = ('course_bind',)
    search_fields = ('lesson_title',)
