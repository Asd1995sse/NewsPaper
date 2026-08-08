from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.conf import settings
from .models import Post


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
    for user in subscribers:
        try:
            html_content = render_to_string(
                'email/new_post_notification.html',
                {
                    'user': user,
                    'post': instance,
                    'site_url': 'http://127.0.0.1:8000',
                }
            )

            send_mail(
                subject=instance.title,
                message=f'Здравствуй, {user.username}. Новая статья в твоём любимом разделе!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=False,
            )
        except Exception as e:
            print(f'Ошибка: {e}')
