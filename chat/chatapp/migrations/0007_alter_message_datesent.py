# Generated by Django 4.1.1 on 2022-12-22 16:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0006_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='dateSent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 22, 16, 11, 45, 464542)),
        ),
    ]
