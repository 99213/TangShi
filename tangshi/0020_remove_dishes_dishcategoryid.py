# Generated by Django 3.1.2 on 2020-11-24 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0019_auto_20201124_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dishes',
            name='DishCategoryId',
        ),
    ]
