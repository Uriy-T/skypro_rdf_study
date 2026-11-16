from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import CourseModel, LessonModel


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()

    class Meta:
        model = CourseModel
        fields = ['course_title',
                  'course_preview',
                  'description',
                  'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

class LessonSerializer(ModelSerializer):

    class Meta:
        model = LessonModel
        fields = '__all__'