# Generated by Django 4.2.18 on 2025-02-01 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_profile_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='applied',
            name='application_status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Under review', 'Under review'), ('Rejected', 'Rejected'), ('Shortlisted', 'Shortlisted')], default='Applied', max_length=30),
        ),
    ]
