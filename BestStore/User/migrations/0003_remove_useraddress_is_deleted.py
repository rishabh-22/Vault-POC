# Generated by Django 2.2.1 on 2019-06-13 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_useraddress'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='is_deleted',
        ),
    ]
