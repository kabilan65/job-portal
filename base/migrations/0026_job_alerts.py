# Generated by Django 4.2.18 on 2025-02-22 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0025_comment_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job_alerts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_type', models.CharField(choices=[('full-time', 'full-time'), ('part-time', 'part-time'), ('remote', 'remote'), ('internship', 'internship')], max_length=100)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('keyword', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
