# Generated by Django 4.1.7 on 2023-03-27 17:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_customtoken_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customtoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 27, 19, 10, 46, 469774, tzinfo=datetime.timezone.utc)),
        ),
    ]
