# Generated by Django 3.1 on 2022-07-23 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20220223_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='tasks.task'),
        ),
    ]
