# Generated by Django 3.1.2 on 2020-12-08 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0023_auto_20201208_1448'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradecomment',
            name='IsWorker',
        ),
        migrations.AddField(
            model_name='tradecomment',
            name='WorkerId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trytest.worker'),
        ),
    ]
