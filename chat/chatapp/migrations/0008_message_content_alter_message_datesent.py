# Generated by Django 4.1.1 on 2022-12-22 16:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0007_alter_message_datesent'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='message',
            name='dateSent',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 22, 16, 24, 3, 642957)),
        ),
    ]
