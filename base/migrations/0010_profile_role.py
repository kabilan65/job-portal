# Generated by Django 4.2.18 on 2025-01-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_remove_applied_title_remove_applied_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('Job Seeker', 'Job Seeker'), ('Recruiter', 'Recruiter')], default='Job Seeker', max_length=20),
        ),
    ]
