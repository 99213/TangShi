# Generated by Django 3.1.2 on 2020-10-28 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0003_auto_20201020_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='OrderTime',
            field=models.TimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='PhoneNumber',
            field=models.IntegerField(max_length=20),
        ),
    ]
