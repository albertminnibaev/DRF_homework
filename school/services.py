from django.conf import settings
from django.core.mail import send_mail

from school.models import Course, Subscription
import stripe
import os


# Рассылка писем пользователям при обновлении курса
def send_order_email(id):
    print(id)
    for item in Course.objects.all():
        print(item.id)
        list_email = []
        if item.id == int(id):
            print(item.subscription.all())
            for item1 in item.subscription.all():
                print(item1.subscriber.email)
                list_email.append(item1.subscriber.email)
                send_mail(
                    subject='Обновление курса',
                    message='Курс, на который вы подписаны обновился. Предлагаем посмотреть обновление на нашем сайте .',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[item1.subscriber.email]
                    #recipient_list=['albert.minnibaeff@yandex.ru']
                )
        print(list_email)


# Напрвление письма на почту пользователя при создании подписки
def send_order_email_subscription_active(email, title):
    send_mail(
        subject=f'Подписка на курс {title}',
        message=f'Вы подписались наполучение рассылки об обновлении курса {title}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
        #recipient_list=['albert.minnibaeff@yandex.ru']
    )


# # Напрвление письма на почту пользователя при отключении подписки (пока не смог вывести название курса)
def send_order_email_subscription_deactive(email, pk):
    print(pk)
    print(Subscription.objects.filter(id=pk))
    send_mail(
        subject=f'Отключение подписки',
        message=f'Вы отключили рассылку об обновлении курса',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
        #recipient_list=['albert.minnibaeff@yandex.ru']
    )


# Функция для получения URL адреса для оплаты
def payments_url(obj):

    stripe.api_key = os.getenv("STRIPE_API_KEY") #sk_test_4eC39HqLyjWDarjtT1zdp7dc"

    product = stripe.Product.create(name=obj.course.title)

    price = stripe.Price.create(
        unit_amount=obj.money,
        currency="usd",
        #recurring={"interval": "month"}, # для периодической оплаты, тогда нужно указать mode="payment" в платеже
        product=product['id'],
        #product="prod_OyEFWEJxeuj4kp",
    )

    paiment = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[
            {
                "price": price['id'],
                "quantity": 1,
            },
        ],
        mode="payment", # для периодической оплаты, тогда нужно указать mode="payment" в платеже
        #mode="subscription",  # для периодической оплаты при recurring={"interval": "month"} в цене
    )

    return paiment['url']
