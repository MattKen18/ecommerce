# Generated by Django 3.0.8 on 2020-09-07 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0019_auto_20200906_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tier',
            field=models.CharField(choices=[('T1', 'Tier 1'), ('T2', 'Tier 2'), ('T3', 'Tier 3')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='vouches',
            field=models.IntegerField(default=0),
        ),
    ]
