# Generated by Django 3.1.2 on 2020-11-25 06:40

from django.db import migrations, models
import trytest.models


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0018_dishes_dishcategoryid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('WorkerName', models.CharField(max_length=10)),
                ('WorkerPosition', models.CharField(max_length=10)),
                ('PhoneNumber', models.FloatField(max_length=20)),
                ('Password', models.CharField(max_length=20)),
                ('Photo', models.ImageField(null=True, upload_to=trytest.models.load_worker_photo)),
            ],
        ),
    ]
