from django.conf import settings
from django.db import models

from users.models import NULLABLE, User


class Course(models.Model):
    title = models.CharField(max_length=250, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='изображение')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='создатель')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=250, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='lesson/', **NULLABLE, verbose_name='изображение')
    video = models.CharField(max_length=250, **NULLABLE, verbose_name='ссылка на видео')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='lesson')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='создатель')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    payment_method = (('наличные', 'наличные'), ('перевод на счет', 'перевод на счет'),)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь', related_name='payments')
    data = models.DateField(verbose_name='дата оплаты')

    course = models.ForeignKey(Course, verbose_name='курс', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='payments')
    lesson = models.ForeignKey(Lesson, verbose_name='урок', on_delete=models.SET_NULL, blank=True, null=True,
                               related_name='payments')

    money = models.PositiveIntegerField(verbose_name='сумма оплаты')
    method = models.CharField(default='наличные', max_length=30, choices=payment_method, verbose_name='метод оплаты')

    def __str__(self):
        return f'{self.data} {self.money} ({self.user})'

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'
