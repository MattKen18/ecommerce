# Generated by Django 3.0.8 on 2020-08-22 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_solditem_product_total'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solditem',
            name='details',
        ),
        migrations.RemoveField(
            model_name='solditem',
            name='name',
        ),
        migrations.RemoveField(
            model_name='solditem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='solditem',
            name='product_total',
        ),
    ]