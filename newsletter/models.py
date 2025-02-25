from django.db import models
from django.utils import timezone

from config import settings


class Client(models.Model):
    '''Модель клиента представляет собой контактные данные о человеке, который должен будет получать рассылки'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя клиента',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия клиента',
    )
    middle_name = models.CharField(
        max_length=50,
        verbose_name='Отчество клиента',
    )
    email = models.EmailField(
        unique=False,
        verbose_name='Email'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    comment = models.TextField(
        verbose_name='комментарий',
        blank=True,
        null=True
    )

    def __str__(self):
        return (f'{self.last_name} {self.first_name} {self.middle_name} ({self.email})\n{self.comment}')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return (f'{self.last_name} {self.first_name} {self.middle_name} ({self.email})')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Message(models.Model):
    '''Модель сообщения'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    title = models.CharField(
        max_length=50,
        verbose_name='тема сообщения'
    )
    message = models.TextField(
        verbose_name='введите сообщение'
    )

    def __str__(self):
        return (f'{self.title}\n{self.message}')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщении'


class Newsletter(models.Model):
    '''Создаем модель рассылки, в которой у нас будет дата и время первой отправки рассылки
    периодичность, статус'''
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    PERIOD_CHOICES = [
        ('day', 'Раз в день'),
        ('week', 'Раз в неделю'),
        ('month', 'Раз в месяц'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    scheduled_at = models.DateTimeField(
        verbose_name='Дата отправки'
    )
    periodicity = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        verbose_name='Переодичность',
    )
    last_run = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Последний запуск',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус',
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        verbose_name='Сообщение',
    )
    clients = models.ManyToManyField(
        Client,
        verbose_name='Клиенты',
    )

    def __str__(self):
        return (f'ID: {self.id} Дата отправки: {self.scheduled_at} Статуc: {self.status}')

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('can_change_newsletter_status', 'Can change newsletter status'),
        ]


class NewsletterAttempt(models.Model):
    '''Модель попытки рассылки'''
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failure', 'Неуспешно'),
    ]

    newsletter = models.ForeignKey(
        Newsletter,
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
        related_name='attempts'
    )
    attempt_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время попытки'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        verbose_name='Статус попытки'
    )
    server_response = models.TextField(
        verbose_name='Ответ почтового сервера',
        blank=True,
        null=True
    )

    def __str__(self):
        return f'Рассылка {self.newsletter.id} - {self.get_status_display()} - {self.attempt_date}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'