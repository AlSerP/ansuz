# Generated by Django 3.1 on 2022-02-23 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_auto_20220206_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='tasks.theme'),
        ),
    ]
