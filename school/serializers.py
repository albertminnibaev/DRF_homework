from rest_framework import serializers

from school.models import Course, Lesson, Payments


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


# сериализатор для просмотра модели курса с полем вывода количества уроков.
class CourseListSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, obj):
        return obj.lesson.count()

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
