# Generated by Django 3.1 on 2022-08-06 14:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20220723_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='mark',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
