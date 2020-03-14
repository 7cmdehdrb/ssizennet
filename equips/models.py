from django.db import models
from django.shortcuts import reverse
from core import models as core_models

# Create your models here.


class AbstractItem(core_models.TimeStampedModel):

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Equip(core_models.TimeStampedModel):

    """ Equip Model Define """

    EQUIPTYPE_CAMCODER = "1camcoder"
    EQUIPTYPE_ACAMCODER = "2camcoac"
    EQUIPTYPE_CAMERA = "3camera"
    EQUIPTYPE_ACAMERA = "4cameraac"
    EQUIPTYPE_ACCESSORY = "5accessory"
    EQUIPTYPE_SOUND = "6sound"
    EQUIPTYPE_TEST = "test"

    EQUIPTYPE_CHOICES = (
        (EQUIPTYPE_CAMCODER, "캠코더"),
        (EQUIPTYPE_ACAMCODER, "캠코더/악세서리"),
        (EQUIPTYPE_CAMERA, "카메라"),
        (EQUIPTYPE_ACAMERA, "카메라/악세서리"),
        (EQUIPTYPE_ACCESSORY, "악세서리"),
        (EQUIPTYPE_SOUND, "음향장비"),
        (EQUIPTYPE_TEST, "테스트"),
    )

    name = models.CharField(max_length=50, null=True)
    serial_number = models.CharField(max_length=20, null=True)
    # equiptype = models.ForeignKey(
    #     Equiptype, related_name="equiptype", on_delete=models.SET_NULL, null=True,
    # )
    equiptype = models.CharField(
        choices=EQUIPTYPE_CHOICES, max_length=20, default=EQUIPTYPE_CAMERA
    )
    enable = models.BooleanField(default=True)
    explain = models.TextField(default="", null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to="equip-photo")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("equips:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = [
            "equiptype",
            "name",
        ]
