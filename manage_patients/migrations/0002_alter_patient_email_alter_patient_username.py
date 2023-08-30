# Generated by Django 4.1.1 on 2023-08-30 05:27

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=254, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='patient',
            name='username',
            field=models.CharField(default='', error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
    ]
