# Generated by Django 3.1.2 on 2020-11-02 08:32

from django.db import migrations, models
import trytest.models


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0011_favoritedish'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='UserImage',
            field=models.ImageField(null=True, upload_to=trytest.models.load_user_image),
        ),
    ]
