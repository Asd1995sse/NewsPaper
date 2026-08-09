from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


@shared_task
def send_notification_email(user_email, username, post_id, post_title, post_content, site_url):
    """Асинхронная отправка письма о новой новости/статье"""
    try:
        # Формируем URL ДО отправки
        post_url = f'{site_url}/news/{post_id}/'

        html_content = render_to_string(
            'email/new_post_notification.html',
            {
                'username': username,
                'post_title': post_title,
                'post_content': post_content[:50],
                'post_url': post_url,
                'site_url': site_url,
            }
        )

        send_mail(
            subject=post_title,
            message=f'Здравствуй, {username}. Новая статья в твоём любимом разделе!\n\nЧитать: {post_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            html_message=html_content,
            fail_silently=False,
        )
        return f'Письмо отправлено {user_email}'
    except Exception as e:
        return f'Ошибка: {e}'

@shared_task
def send_weekly_newsletter():
    """Еженедельная рассылка (запускается по расписанию)"""
    from django.utils import timezone
    from datetime import timedelta

    week_ago = timezone.now() - timedelta(days=7)
    categories = Category.objects.filter(subscribers__isnull=False).distinct()

    for category in categories:
        posts = Post.objects.filter(
            categories=category,
            created_at__gte=week_ago,
            post_type=Post.NEWS
        ).order_by('-created_at')

        if not posts:
            continue

        for user in category.subscribers.all():
            html_content = render_to_string(
                'news/email/weekly_newsletter.html',
                {
                    'user': user,
                    'category': category,
                    'posts': posts,
                    'site_url': 'http://127.0.0.1:8000',
                }
            )

            send_mail(
                subject=f'Новости за неделю в разделе "{category.name}"',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_content,
                fail_silently=False,
            )

    return 'Еженедельная рассылка отправлена'