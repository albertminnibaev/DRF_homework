from rest_framework import serializers

from school.models import Course, Lesson, Payments, Subscription
from school.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            VideoValidator(field='video')
        ]


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


# сериализатор для просмотра модели курса с полем вывода количества уроков.
class CourseListSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)
    lesson = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, obj):
        return obj.lesson.count()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
