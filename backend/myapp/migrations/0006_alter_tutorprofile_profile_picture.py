# Generated by Django 4.1.7 on 2024-12-30 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_tutorprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorprofile',
            name='profile_picture',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
