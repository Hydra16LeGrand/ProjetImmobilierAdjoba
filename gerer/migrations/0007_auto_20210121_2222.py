# Generated by Django 3.0.7 on 2021-01-21 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerer', '0006_auto_20210121_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bien',
            name='image',
            field=models.ImageField(blank=True, upload_to='bien'),
        ),
    ]
