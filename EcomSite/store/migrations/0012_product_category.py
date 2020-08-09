# Generated by Django 3.0.8 on 2020-08-06 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_address_zip_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('TB', 'textbook'), ('NB', 'notebook'), ('SB', 'school reading book'), ('RB', 'reading book')], max_length=10, null=True),
        ),
    ]
