from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="min")
        if not admin:
            User.objects.create_superuser("min", "7cmdehdrb@naver.com", "cdkey0246@@")
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
