# Generated by Django 4.2.5 on 2023-09-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_member_email_alter_member_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(error_messages={'code': 'invalid email', 'unique': 'Email id must be unique'}, max_length=254, unique=True),
        ),
    ]
