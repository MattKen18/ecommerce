# Generated by Django 3.0.8 on 2020-10-11 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_auto_20201011_1826'),
        ('seller', '0028_auto_20201011_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='vouches',
            field=models.ManyToManyField(blank=True, null=True, to='store.Customer'),
        ),
    ]
