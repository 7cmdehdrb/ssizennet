import os
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.create_superuser("minmin", "myuser@myemail.com", "cdkeypass0246")

