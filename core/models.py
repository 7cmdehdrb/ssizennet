from django.db import models
from . import managers

# Create your models here.


class TimeStampedModel(models.Model):

    """Time Stamped Model """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = managers.CustomModelManager()

    # if I write auto_now = True inside of DataTimeField,
    # Field will record date and time when it save model
    # Also, if I write auto_now_add = True inside of DataTimeField,
    # Field will be updated whenever it creates models

    class Meta:
        abstract = True
        # not save to database. only use for code
