# Generated by Django 3.0.8 on 2020-08-22 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20200822_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='solditem',
            name='product_total',
            field=models.IntegerField(default=1),
        ),
    ]
