from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from news.models import Post


class Command(BaseCommand):
    help = 'Создаёт группы и права для проекта'

    def handle(self, *args, **options):
        # Группа common
        common_group, _ = Group.objects.get_or_create(name='common')

        # Группа authors
        authors_group, _ = Group.objects.get_or_create(name='authors')

        # Права для модели Post
        content_type = ContentType.objects.get_for_model(Post)
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['add_post', 'change_post', 'delete_post']
        )

        authors_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Группы и права успешно созданы'))