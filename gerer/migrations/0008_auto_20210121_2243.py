# Generated by Django 3.0.7 on 2021-01-21 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerer', '0007_auto_20210121_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maison',
            name='utilisateur',
        ),
        migrations.RemoveField(
            model_name='terrain',
            name='utilisateur',
        ),
    ]
