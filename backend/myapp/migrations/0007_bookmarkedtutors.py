# Generated by Django 4.1.7 on 2025-01-04 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_tutorprofile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookmarkedTutors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('tutor_id', models.IntegerField()),
            ],
        ),
    ]
