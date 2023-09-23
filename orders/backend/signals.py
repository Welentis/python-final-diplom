from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver, Signal

from .models import ConfirmEmailToken, User

new_user_registered = Signal('user_id',)

new_order = Signal('user_id',)


@receiver(new_user_registered)
def new_user_registered_signal(user_id, **kwargs):
    """
    отправляем письмо с подтрердждением почты
    """
    # send an e-mail to the user
    token, _ = ConfirmEmailToken.objects.get_or_create(user_id=user_id)

    # msg = EmailMultiAlternatives(
    #     # title:
    #     f"Password Reset Token for {token.user.email}",
    #     # message:
    #     token.key,
    #     # from:
    #     settings.EMAIL_HOST_USER,
    #     # to:
    #     [token.user.email]
    # )
    # msg.send()
    user = User.objects.get(id=user_id)
    subject = 'Email Confirmation'
    to = [user.email, ]
    body = f"Your registration was successful. Your username: {user.username}, your password: {user.password}"
    message = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=to)
    message.send()



@receiver(new_order)
def new_order_signal(user_id, **kwargs):
    """
    отправяем письмо при изменении статуса заказа
    """
    # send an e-mail to the user
    user = User.objects.get(id=user_id)

    msg = EmailMultiAlternatives(
        # title:
        f"Обновление статуса заказа",
        # message:
        'Заказ сформирован',
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [user.email]
    )
    msg.send()
