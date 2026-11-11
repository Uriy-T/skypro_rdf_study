from django.db import models


class CourseModel(models.Model):
    course_title = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название курса'
    )
    course_preview = models.ImageField(
        upload_to='courses/previews/',
        null=True,
        blank=True,
        verbose_name='Превью курса'
    )
    description = models.TextField(
        null=True,
        verbose_name='Описание курса'
    )

    def __str__(self):
        return self.course_title

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class LessonModel(models.Model):
    lesson_title = models.CharField(
        max_length=200,
        null=False,
        verbose_name='Название урока'
    )
    description = models.TextField(
        max_length=1000,
        null=True,
        verbose_name='Описание урока'
    )
    lesson_preview = models.ImageField(
        upload_to='lessons/previews/',
        null=True,
        blank=True,
        verbose_name='Превью урока'
    )
    video_link = models.URLField(
        verbose_name='Ссылка на видео'
    )
    course_bind = models.ForeignKey(
        CourseModel,
        null=True,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
