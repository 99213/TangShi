# Generated by Django 3.1.2 on 2020-10-30 20:56

from django.db import migrations, models
import trytest.models


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0009_auto_20201030_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proposalimage',
            name='Picture',
            field=models.ImageField(blank=True, null=True, upload_to=trytest.models.load_proposal_image),
        ),
    ]
