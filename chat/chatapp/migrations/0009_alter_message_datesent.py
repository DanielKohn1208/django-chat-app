# Generated by Django 4.1.1 on 2022-12-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0008_message_content_alter_message_datesent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='dateSent',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
