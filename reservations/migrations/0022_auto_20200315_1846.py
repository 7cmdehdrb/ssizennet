# Generated by Django 2.2.5 on 2020-03-15 18:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0021_auto_20200316_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='catagory',
            field=models.CharField(choices=[('info', '정보'), ('school', '교내행사'), ('refine', '교양'), ('realiy', '예능'), ('perform', '공연'), ('radio', '라디오'), ('surv', '영상제'), ('personal', '개인')], default='info', max_length=10),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='check_in',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 15, 18, 46, 46, 913563)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='check_out',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 15, 18, 46, 46, 913563)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserv_code',
            field=models.CharField(blank=True, default='5f09', max_length=4),
        ),
    ]
