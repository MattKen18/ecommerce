# Generated by Django 3.0.8 on 2020-08-07 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_auto_20200807_1816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='home',
        ),
        migrations.AddField(
            model_name='homeaddress',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.Profile'),
        ),
    ]
