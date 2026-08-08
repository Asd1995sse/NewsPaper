from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        html_content = render_to_string(
            'sign/email/welcome.html',
            {'user': instance}
        )

        send_mail(
            subject='Добро пожаловать на News Portal!',
            message=f'Добрый день, {instance.username}! Благодарим вас за регистрацию.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=html_content,
            fail_silently=True,
        )