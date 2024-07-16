from celery import shared_task
import time
from datetime import datetime, timedelta

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed, pre_init
from .models import Post, PostCategory, SubscriptionsCategory, User


 @shared_task
 #Реализовать рассылку уведомлений подписчикам после создания новости.
def mailing():
    def send_notifications(preview, pk, title, subscribers):
        html_content = render_to_string(
             'post_created_email.html',
             {
                 'text': preview,
                 'link': f'{settings.SITE_URL}main/{pk}'

             }
         )
        msg = EmailMultiAlternatives(
             subject=title,
             body='',
             from_email=settings.DEFAULT_FROM_EMAIL,
             to=subscribers
         )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @receiver(m2m_changed, sender=PostCategory)
    def notify_about_new_post(sender, instance, **kwargs):
         if kwargs['action'] == 'post_add':
             subscribers_emails = User.objects.filter(subscriptions__in=instance.categories.all()).values_list('email',
                                                                                                               flat=True)
             print(subscribers_emails)

             send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)

@shared_task
# Реализовать еженедельную рассылку с последними новостями (каждый понедельник в 8:00 утра)
def newsletter_every_week():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(date_time_creation_post__gte=last_week)
    subscribers = User.objects.all().values_list('email', flat=True)

    html_content = render_to_string(
        'weekly_post.html',
        {
            'posts': posts,
            'link': settings.SITE_URL
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()