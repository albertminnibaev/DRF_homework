from datetime import datetime, timedelta

import pytz
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from school.models import Course
from users.models import User


# Рассылка писем пользователям при обновлении курса
@shared_task
def send_order_email(id):
    for item in Course.objects.all():
        list_email = []
        if item.id == int(id):
            for item1 in item.subscription.all():
                list_email.append(item1.subscriber.email)
                try:
                    send_mail(
                        subject='Обновление курса',
                        message='Курс, на который вы подписаны обновился. Предлагаем посмотреть обновление на нашем сайте .',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=['albert.minnibaeff@yandex.ru']
                        # recipient_list=[item1.subscriber.email]
                    )
                except:
                    print(f'Не удалось отравить сообщение на адрес "{item1.subscriber.email}"')


# Напрвление письма на почту пользователя при создании подписки
@shared_task
def send_order_email_subscription_active(email, title):
    try:
        send_mail(
            subject=f'Подписка на курс {title}',
            message=f'Вы подписались наполучение рассылки об обновлении курса {title}',
            from_email=settings.EMAIL_HOST_USER,
            # recipient_list=[email]
            recipient_list=['albert.minnibaeff@yandex.ru']
        )
    except:
        print(f'Не удалось отравить сообщение на адрес "{email}"')


# # Напрвление письма на почту пользователя при отключении подписки (пока не смог вывести название курса)
@shared_task
def send_order_email_subscription_deactive(email, pk):
    try:
        send_mail(
            subject=f'Отключение подписки',
            message=f'Вы отключили рассылку об обновлении курса',
            from_email=settings.EMAIL_HOST_USER,
            # recipient_list=[email]
            recipient_list=['albert.minnibaeff@yandex.ru']
        )
    except:
        print(f'Не удалось отравить сообщение на адрес "{email}"')


# Функция блокировки ползователя, если пользователь не заходил более месяца (30 дней)
@shared_task
def user_active():
    for user in User.objects.all():
        if user.last_login:
            delta = datetime.now(pytz.utc) - user.last_login
            if delta.days > 30:
                user.is_active = False
                user.save()
