# Generated by Django 3.0.4 on 2020-03-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equips', '0014_auto_20200313_2001'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equip',
            options={'ordering': ['equiptype', 'name']},
        ),
        migrations.AlterField(
            model_name='equip',
            name='equiptype',
            field=models.CharField(choices=[('camcoder', '캠코더'), ('acamcoder', '캠코더/악세서리'), ('amera', '카메라'), ('acamera', '카메라/악세서리'), ('accessory', '악세서리'), ('sound', '음향장비'), ('test', '테스트')], default='amera', max_length=20),
        ),
    ]
