# Generated by Django 3.0.8 on 2020-08-02 02:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0006_auto_20200728_1802'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line1', models.CharField(max_length=200, null=True)),
                ('address_line2', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=200, null=True)),
                ('country', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='shipping',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='orderID',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='total',
        ),
        migrations.RemoveField(
            model_name='product',
            name='seller',
        ),
        migrations.AddField(
            model_name='customer',
            name='seller',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='store.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='store.Customer'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='store.Product'),
        ),
        migrations.DeleteModel(
            name='HomeAddress',
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
        migrations.DeleteModel(
            name='Shipping',
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Customer'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
