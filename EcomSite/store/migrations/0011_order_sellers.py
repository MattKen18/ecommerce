# Generated by Django 3.0.8 on 2020-08-22 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_order_singleitems'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='sellers',
            field=models.ManyToManyField(to='store.Customer'),
        ),
    ]
