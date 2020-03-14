# Generated by Django 3.0.4 on 2020-03-13 19:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0013_auto_20200313_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='check_in',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 13, 19, 19, 43, 732622)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='check_out',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 13, 19, 19, 43, 732622)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserv_code',
            field=models.CharField(blank=True, default='e2fee4539f324484bb90', max_length=20),
        ),
    ]
