# Generated by Django 3.0.8 on 2020-10-11 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_auto_20201003_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solditem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/%Y/%m/%d/'),
        ),
    ]
