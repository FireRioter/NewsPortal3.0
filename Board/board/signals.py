from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Response

@receiver(post_save, sender=Response)
def notify_user_response(sender, instance, created, **kwargs):
    if created:
        # Уведомление пользователя о новом отклике
        ad_owner = instance.ad.user
        subject = f"Новый отклик на ваше объявление: {instance.ad.title}"
        message = f"Вы получили новый отклик от {instance.user.email}.\n\nСодержание отклика:\n{instance.content}"
        send_mail(subject, message, 'ruslanSkillFactory@yandex.ru', [ad_owner.email])

@receiver(post_save, sender=User)
def welcome_email(sender, instance, created, **kwargs):
    if created:
        # Отправка приветственного письма новому пользователю
        subject = "Добро пожаловать на наш сайт"
        message = f"Здравствуйте, {instance.username}!\n\nСпасибо за регистрацию на нашем сайте."
        send_mail(subject, message, 'ruslanSkillFactory@yandex.ru', [instance.email])