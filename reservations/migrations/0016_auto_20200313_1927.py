# Generated by Django 3.0.4 on 2020-03-13 19:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0015_auto_20200313_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='check_in',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 13, 19, 27, 18, 76109)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='check_out',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 13, 19, 27, 18, 76109)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserv_code',
            field=models.CharField(blank=True, default='01da5067743b424e9272', max_length=20),
        ),
    ]
