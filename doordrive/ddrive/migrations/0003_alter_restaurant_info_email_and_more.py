# Generated by Django 5.1.1 on 2024-11-04 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddrive', '0002_user_is_active_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant_info',
            name='email',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='restaurant_info',
            name='phone_number',
            field=models.CharField(max_length=15),
        ),
    ]
