# Generated by Django 3.0.8 on 2020-08-22 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0008_pickup'),
    ]

    operations = [
        migrations.AddField(
            model_name='pickup',
            name='phone',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='pickup',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
