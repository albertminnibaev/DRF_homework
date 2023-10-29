from datetime import date
from random import randint, choice

from django.core.management import BaseCommand

from school.models import Payments, Course, Lesson
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        year = randint(2020, 2022)
        month = randint(1, 12)
        day = randint(1, 28)
        random_date = date(year, month, day)
        payment_method = choice(('наличные', 'перевод на счет'))
        choice_1 = randint(0, 1)
        if choice_1:
            course = Course.objects.all().order_by('?').first()
            lesson = None
        else:
            course = None
            lesson = Lesson.objects.all().order_by('?').first()
        payments = Payments.objects.create(
            user=User.objects.all().order_by('?').first(),
            data=random_date,
            course=course,
            lesson=lesson,
            money=randint(1, 100),
            method=payment_method,
        )

        payments.save()
