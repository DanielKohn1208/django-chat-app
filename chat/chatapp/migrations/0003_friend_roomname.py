# Generated by Django 4.1.1 on 2022-10-30 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_rename_friendship_friend'),
    ]

    operations = [
        migrations.AddField(
            model_name='friend',
            name='roomName',
            field=models.CharField(default='help', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
