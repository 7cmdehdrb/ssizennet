# Generated by Django 3.0.3 on 2020-02-24 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='accept',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='catagory',
            field=models.CharField(choices=[('info', '정보'), ('school', '교내행사'), ('refine', '교양'), ('reality', '예능'), ('perform', '공연'), ('radio', '라디오'), ('surv', '영상제')], default='', max_length=10),
        ),
        migrations.AddField(
            model_name='reservation',
            name='purpose',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('before', '대여전'), ('now', '대여중'), ('finish', '반납완료')], default='before', max_length=10),
        ),
    ]
