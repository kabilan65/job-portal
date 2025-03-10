# Generated by Django 4.2.18 on 2025-01-27 13:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0008_applied_alter_post_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applied',
            name='title',
        ),
        migrations.RemoveField(
            model_name='applied',
            name='username',
        ),
        migrations.AddField(
            model_name='applied',
            name='applied_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applied',
            name='post',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='base.post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applied',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
