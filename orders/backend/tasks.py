from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from rest_framework.authtoken.models import Token
from .models import ConfirmEmailToken, User
from celery import shared_task


@shared_task
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    # token, _ = ConfirmEmailToken.objects.create(user_id=user_id)
    token_new = Token.objects.get(user=user_id)
    user = User.objects.get(id=user_id)
    subject = 'Email Confirmation'
    to = [user.email, ]
    body = f"Your registration was successful. Your username: {user.username}, your token: Token {token_new.key}"
    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to)
    message.send()


@shared_task
def new_order_signal(user_id, **kwargs):
    # send an e-mail to the user
    user = User.objects.get(id=user_id)
    subject = 'Обновление статуса заказа'
    to = [user.email]
    body = "Заказ сформирован"
    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to
    )
    message.send()
