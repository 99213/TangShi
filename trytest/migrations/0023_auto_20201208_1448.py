# Generated by Django 3.1.2 on 2020-12-08 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0022_auto_20201208_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradecomment',
            name='Reply',
        ),
        migrations.AddField(
            model_name='tradecomment',
            name='IsWorker',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tradecomment',
            name='ReplyId',
            field=models.IntegerField(max_length=200, null=True),
        ),
    ]
