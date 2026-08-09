from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.conf import settings
from .models import Post
from .tasks import send_notification_email

@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action != 'post_add':
        return

    if instance.post_type not in [Post.NEWS, Post.ARTICLE]:
        return

    # Получаем категории
    categories = instance.categories.all()

    if not categories:
        return

    # Собираем подписчиков
    subscribers = set()
    for category in categories:
        for user in category.subscribers.all():
            subscribers.add(user)
    if not subscribers:
        return

    # Отправляем письма
    site_url = 'http://127.0.0.1:8000'
    for user in subscribers:
        send_notification_email.delay(
            user_email=user.email,
            username=user.username,
            post_id=instance.id,
            post_title=instance.title,
            post_content=instance.content,
            site_url=site_url,
        )


