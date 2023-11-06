from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from school.models import Course, Lesson, Subscription
from school.views import LessonCreateAPIView
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:

        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test'
        )

        self.lesson = Lesson.objects.create(
            title='test',
            description='test',
            course=self.course,
            video='https://www.youtube.com/'
        )

    def test_create_lesson(self):
        """ Тестирование создания урока """

        data = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'video': self.lesson.video,
            'course': self.course.id
        }

        response = self.client.post(
            '/school/lesson/create/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'id': (self.lesson.id + 1), 'title': self.lesson.title, 'description': self.lesson.description,
             'preview': None, 'video': self.lesson.video, 'course': self.course.id, 'creator': self.user.id}
        )
        self.assertTrue(
            Lesson.objects.all().exists()
        )

    def test_list_lesson(self):
        """ Тестирование просмотра списка уроков """

        response = self.client.get(
            '/school/lesson/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json()['results'],
            [{'id': self.lesson.id, 'title': self.lesson.title, 'description': self.lesson.description,
             'preview': None, 'video': self.lesson.video, 'course': self.course.id, 'creator': None}]
        )

    def test_retrieve_lesson(self):
        """ Тестирование просмотра одного урока """

        # создаем новый урок авторизированным пользователем
        data_1 = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'video': self.lesson.video,
            'course': self.course.id
        }

        response = self.client.post(
            '/school/lesson/create/',
            data=data_1
        )

        # запрос на просмотр урока
        response = self.client.get(
            f'/school/lesson/{(self.lesson.id + 1)}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'id': (self.lesson.id + 1), 'title': self.lesson.title, 'description': self.lesson.description,
             'preview': None, 'video': self.lesson.video, 'course': self.course.id, 'creator': self.user.id}
        )

    def test_update_lesson(self):
        """ Тестирование обновления урока """

        # создаем новый урок авторизированным пользователем
        data_1 = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'video': self.lesson.video,
            'course': self.course.id
        }

        response = self.client.post(
            '/school/lesson/create/',
            data=data_1
        )

        # запрос на обновление урока
        data = {
            'title': 'test_updated',
            'video': 'https://www.youtube.com/dfdf'
        }
        response = self.client.patch(
            f'/school/lesson/update/{self.lesson.id + 1}/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': (self.lesson.id + 1), 'title': 'test_updated', 'description': self.lesson.description,
             'preview': None, 'video': 'https://www.youtube.com/dfdf', 'course': self.course.id, 'creator': self.user.id}
        )

    def test_destroy_lesson(self):
        """ Тестирование удаления урока """

        # создаем новый урок авторизированным пользователем
        data_1 = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'video': self.lesson.video,
            'course': self.course.id
        }

        response = self.client.post(
            '/school/lesson/create/',
            data=data_1
        )

        response = self.client.delete(
            f'/school/lesson/delete/{self.lesson.id + 1}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='test@test.com', password='test', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
        )
        self.subscription = Subscription.objects.create(
            course=self.course,
        )

    def test_create_subscription(self):
        """ Тестирование создания подписки """

        data = {
            'course': self.course.id,
        }
        response = self.client.post(
            '/school/subscription/create/',
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {'id': (self.subscription.id + 1), 'subscriber': self.user.id, 'course': self.course.id}
        )
        self.assertTrue(
            Subscription.objects.all().exists()
        )

    def test_destroy_subscription(self):
        """ Тестирование удаления подписки """

        response = self.client.delete(
            f'/school/subscription/delete/{self.subscription.id}/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )







