# Generated by Django 5.1.1 on 2024-11-03 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dasher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dasher_id', models.CharField(max_length=10, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('pickup_phone_number', models.CharField(max_length=15)),
                ('dropoff_phone_number', models.CharField(max_length=15)),
                ('vehicle_make', models.CharField(max_length=100)),
                ('vehicle_model', models.CharField(max_length=100)),
                ('vehicle_year', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('store_id', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_id', models.CharField(max_length=10)),
                ('pickup_address', models.TextField()),
                ('pickup_phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('refrence_tag', models.TextField()),
                ('dropoff_verification_pic', models.URLField()),
                ('dasher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddrive.dasher')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ddrive.user')),
            ],
        ),
    ]
