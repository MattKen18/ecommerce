import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Customer(models.Model): # a customer is the equivalent of a user
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    seller = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def make_seller(self):
        if self.seller == False:
            self.seller = True
        else:
            pass

    @receiver(post_save, sender=User)
    def create_user_customer(sender, instance, created, **kwargs):
        if created:
            Customer.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_customer(sender, instance, **kwargs):
        instance.customer.save()

    post_save.connect(save_user_customer, sender=User)



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.OneToOneField(Customer, null=True, blank=True, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=200, null=True, blank=False)
    address_line2 = models.CharField(max_length=200, null=True, blank=False) #post office
    state = models.CharField(max_length=200, null=True, blank=False)
    country = models.CharField(max_length=200, null=True, blank=False)


class Product(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=200, null=True, blank=False)
    price = models.FloatField(null=True, blank=False)
    details = models.CharField(max_length=200, null=True, blank=True)
    available = models.BooleanField(default=True, null=True, blank=False) #sold or not

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "'s Cart"


class OrderItem(models.Model): #each item which emulates a cart item
    cart = models.ForeignKey(Cart, null=True, blank=False, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    def total(self):
        return self.quantity * self.product.price


class Order(models.Model): #emulates cart cashout
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    order_date = models.DateTimeField(null=True, blank=False)
