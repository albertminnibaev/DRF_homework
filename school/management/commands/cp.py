from django.core.management import BaseCommand

from school.models import Payments, Course
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        payments = Payments.objects.create(
            user=User.objects.get(pk=1),
            data='2023-11-23',
            course=Course.objects.get(pk=2),
            money=1000,
        )

        payments.save()
