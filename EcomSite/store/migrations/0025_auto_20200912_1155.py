# Generated by Django 3.0.8 on 2020-09-12 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0023_auto_20200911_0859'),
        ('store', '0024_auto_20200831_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.Profile'),
        ),
    ]
