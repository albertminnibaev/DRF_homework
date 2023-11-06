from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from school.models import Course, Lesson, Payments, Subscription
from school.paginators import CoursePaginator, LessonPaginator
from school.permissions import IsCreator, IsRetrieveCreator
from school.serializers import CourseSerializer, LessonSerializer, CourseListSerializer, PaymentsSerializer, \
    SubscriptionSerializer
from school.services import send_order_email, send_order_email_subscription_active, \
    send_order_email_subscription_deactive
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def list(self, request, *args, **kwargs):
        queryset = Course.objects.all()

        # данный код необходим для того чтобы работала пагинация
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # Метод для вывода информации по курсу с определением выборки из базы и указанием сериализатора
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = CourseListSerializer(course)
        return Response(serializer.data)

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.creator = self.request.user
        new_lesson.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        # функция рассылки писем всем кто подписан на курс, при обновлении курса
        send_order_email(self.kwargs['pk'])

        return self.update(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['create']:
            return [(IsAuthenticated & ~IsModerator)()]
        if self.action in ['destroy']:
            return [IsCreator()]
        if self.action in ['list']:
            return [IsAuthenticated()]
        if self.action in ['retrieve']:
            return [IsRetrieveCreator()]
        # if self.action in ['retrieve', 'update', 'partial_update']:
        #     return [((IsAuthenticated & IsModerator) | (IsAuthenticated & IsCreator))()]

        return [((IsAuthenticated & IsModerator) | (IsAuthenticated & IsCreator))()]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.creator = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LessonPaginator
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsCreator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsCreator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsCreator]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method')
    ordering_fields = ('data',)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def perform_create(self, serializer):
        new_subscription = serializer.save()
        new_subscription.subscriber = self.request.user

        send_order_email_subscription_active(self.request.user.email, new_subscription.course.title)

        new_subscription.save()


class SubscriptionDestroyApiView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()

    def delete(self, request, *args, **kwargs):

        send_order_email_subscription_deactive(self.request.user.email, self.kwargs['pk'])

        return self.destroy(request, *args, **kwargs)
