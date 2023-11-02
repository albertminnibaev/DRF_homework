from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        # user = User.objects.create(
        #     email='1@yandex.ru',
        #     first_name='Admin',
        #     last_name='Adminov',
        #     is_superuser=True,
        #     is_staff=True,
        #     is_active=True
        # )
        # user = User.objects.create(
        #     email='2@yandex.ru',
        #     first_name='Admin',
        #     last_name='Adminov',
        #     is_superuser=False,
        #     is_staff=True,
        #     is_active=True
        # )
        #
        # user.set_password('123qwe456rty')
        # user.save()

        user = User.objects.create(
            email='3@yandex.ru',
            first_name='Admin',
            last_name='Adminov',
            is_superuser=False,
            is_staff=False,
            is_active=True
        )

        user.set_password('123qwe456rty')
        user.save()
