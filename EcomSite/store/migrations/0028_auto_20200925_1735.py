# Generated by Django 3.0.8 on 2020-09-25 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_product_edited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='details',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
