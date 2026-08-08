from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from news.models import Post, Category
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Отправляет еженедельную рассылку новостей'

    def handle(self, *args, **options):
        week_ago = timezone.now() - timedelta(days=7)

        # Находим все категории, на которые кто-то подписан
        categories = Category.objects.filter(subscribers__isnull=False).distinct()

        for category in categories:
            # Находим статьи за неделю в этой категории
            posts = Post.objects.filter(
                categories=category,
                created_at__gte=week_ago,
                post_type=Post.NEWS
            ).order_by('-created_at')

            if not posts:
                continue

            subscribers = category.subscribers.all()

            for user in subscribers:
                html_content = render_to_string(
                    'news/email/weekly_newsletter.html',
                    {
                        'user': user,
                        'category': category,
                        'posts': posts,
                        'week_ago': week_ago,
                        'site_url': 'http://127.0.0.1:8000',
                    }
                )

                send_mail(
                    subject=f'Новости за неделю в разделе "{category.name}"',
                    message=f'Здравствуй, {user.username}! Новые статьи за неделю.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_content,
                    fail_silently=True,
                )

        self.stdout.write(self.style.SUCCESS('Рассылка отправлена'))