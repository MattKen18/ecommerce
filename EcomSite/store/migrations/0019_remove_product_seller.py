# Generated by Django 3.0.8 on 2020-08-08 00:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20200807_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
    ]
