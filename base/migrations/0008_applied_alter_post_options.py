# Generated by Django 4.2.18 on 2025-01-27 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_profile_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('username', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-date_created']},
        ),
    ]
