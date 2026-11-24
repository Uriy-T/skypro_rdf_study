from rest_framework.serializers import ModelSerializer, SerializerMethodField
from courses.models import CourseModel, LessonModel
from courses.validators import VideoLinkValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = LessonModel
        fields = '__all__'
        validators = [VideoLinkValidator(field='video_link')]


class CourseSerializer(ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons_list = LessonSerializer(many=True, read_only=True, source='lessons')

    class Meta:
        model = CourseModel
        fields = ['course_title',
                  'course_preview',
                  'description',
                  'lessons_count',
                  'lessons_list']

    def get_lessons_count(self, obj):
        return obj.lessons.count()
