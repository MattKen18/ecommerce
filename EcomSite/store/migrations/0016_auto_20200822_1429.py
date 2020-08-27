# Generated by Django 3.0.8 on 2020-08-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_solditem_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solditem',
            name='item',
        ),
        migrations.AddField(
            model_name='solditem',
            name='details',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='solditem',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='solditem',
            name='price',
            field=models.FloatField(null=True),
        ),
    ]
