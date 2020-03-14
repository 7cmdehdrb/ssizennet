from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.db import models

# Create your models here.


class User(AbstractUser):

    """ Custom User Model """

    # define departure

    DEPARTURE_DIRECT = "dirc"
    DEPARTURE_WRITE = "writ"
    DEPARTURE_TECH = "tech"
    DEPARTURE_ENTER = "entr"
    DEPARTURE_WEB = "webc"

    DEPARTURE_CHOICES = (
        (DEPARTURE_DIRECT, "연출부"),
        (DEPARTURE_WRITE, "구성작가부"),
        (DEPARTURE_TECH, "방송기술부"),
        (DEPARTURE_ENTER, "엔터테이너부"),
        (DEPARTURE_WEB, "웹컨텐츠부"),
    )

    avatar = models.ImageField(null=True, blank=True, upload_to="avatars")
    departure = models.CharField(choices=DEPARTURE_CHOICES, max_length=6)
    order = models.IntegerField(null=True)
    kakaotalk = models.CharField(max_length=18)
    upperuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def clean_username(self):
        result = self.cleaned_data
        return result

    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"pk": self.pk})
