# Generated by Django 4.2.5 on 2023-09-21 21:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_book_ratings_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Email id must be unique'}, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(message='Enter a valid number', regex=' ^\\d{10}$')]),
        ),
    ]