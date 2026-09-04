import os
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создаёт суперпользователя из переменных окружения, если его нет'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.environ.get('ADMIN_USER', 'admin'),
                password=os.environ.get('ADMIN_PASS', 'admin12345'),
            )
            self.stdout.write(self.style.SUCCESS('Суперпользователь создан!'))