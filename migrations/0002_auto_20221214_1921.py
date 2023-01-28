# Generated by Django 3.2 on 2022-12-14 13:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy_and_sell', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestproduct',
            name='duration_needed',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='requestproduct',
            name='is_for_rental',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='is_for_rental',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='saleproduct',
            name='security_deposit',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)]),
        ),
    ]
