# Generated by Django 3.1.1 on 2025-02-17 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_auto_20250217_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.CharField(choices=[('Ahmedabad', 'Ahmedabad'), ('Bengaluru', 'Bengaluru'), ('Bhopal', 'Bhopal'), ('Bhubaneswar', 'Bhubaneswar'), ('Chandigarh', 'Chandigarh'), ('Chennai', 'Chennai'), ('Coimbatore', 'Coimbatore'), ('Delhi', 'Delhi'), ('Faridabad', 'Faridabad'), ('Ghaziabad', 'Ghaziabad'), ('Gurgaon', 'Gurgaon'), ('Guwahati', 'Guwahati'), ('Hyderabad', 'Hyderabad'), ('Indore', 'Indore'), ('Jaipur', 'Jaipur'), ('Jalandhar', 'Jalandhar'), ('Jamshedpur', 'Jamshedpur'), ('Kanpur', 'Kanpur'), ('Kochi', 'Kochi'), ('Kolkata', 'Kolkata'), ('Lucknow', 'Lucknow'), ('Ludhiana', 'Ludhiana'), ('Madurai', 'Madurai'), ('Meerut', 'Meerut'), ('Mumbai', 'Mumbai'), ('Mysuru', 'Mysuru'), ('Nagpur', 'Nagpur'), ('Nashik', 'Nashik'), ('Noida', 'Noida'), ('Patna', 'Patna'), ('Pune', 'Pune'), ('Raipur', 'Raipur'), ('Rajkot', 'Rajkot'), ('Ranchi', 'Ranchi'), ('Siliguri', 'Siliguri'), ('Surat', 'Surat'), ('Thane', 'Thane'), ('Thrissur', 'Thrissur'), ('Tiruchirapalli', 'Tiruchirapalli'), ('Udaipur', 'Udaipur'), ('Vadodara', 'Vadodara'), ('Varanasi', 'Varanasi'), ('Vijayawada', 'Vijayawada'), ('Visakhapatnam', 'Visakhapatnam'), ('Others', 'Others')], default='Others', max_length=50),
        ),
    ]
