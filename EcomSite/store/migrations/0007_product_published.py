# Generated by Django 3.0.8 on 2020-08-16 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_rejected'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]