# Generated by Django 3.1.2 on 2020-10-30 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trytest', '0008_auto_20201028_1540'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dishes',
            name='DishPic',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='Picture',
        ),
        migrations.CreateModel(
            name='ProposalImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Picture', models.ImageField(null=True, upload_to='picture')),
                ('Proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trytest.proposal')),
            ],
        ),
        migrations.CreateModel(
            name='DishesImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DishPic', models.ImageField(null=True, upload_to='picture')),
                ('Dishes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trytest.dishes')),
            ],
        ),
    ]
