# Generated by Django 3.1.2 on 2020-12-08 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0021_tradedish_commentnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradedish',
            name='CommentNum',
        ),
        migrations.AddField(
            model_name='dishes',
            name='ScoreNum',
            field=models.IntegerField(default=0),
        ),
    ]
