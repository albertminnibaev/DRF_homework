from django.urls import path
from rest_framework.routers import DefaultRouter

from school.apps import SchoolConfig
from school.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentsListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyApiView, PaymentsCreateAPIView

app_name = SchoolConfig.name


router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson_view'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments_create'),

    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name="subscription_create"),
    path('subscription/delete/<int:pk>/', SubscriptionDestroyApiView.as_view(), name='subscription_delete'),
] + router.urls

