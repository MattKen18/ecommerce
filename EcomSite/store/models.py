import datetime
import os
import uuid
from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from seller.models import Profile
from django_countries.fields import CountryField


# Create your models here.

categories = [
        ('TB', 'Textbooks'),
        ('NB', 'Notebooks'),
        ('LB', 'Literature Books'),
        ('RB', 'Reading Books'),

]

conditions = [
        ('BN', 'Brand New'),
        ('NGC', 'New Good Condition'),
        ('NPC', 'New Poor Condition'),
        ('UGD', 'Used Good Condition'),
        ('UPC', 'Used Poor Condition'),
]


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



class Address(models.Model): #shipping address
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=200, null=True, blank=False)
    address_line2 = models.CharField(max_length=200, null=True, blank=False) #post office
    city = models.CharField(max_length=200, null=True, blank=False)
    state = models.CharField(max_length=200, null=True, blank=False)
    zip_code = models.CharField(max_length=200, null=True, blank=False)
    country = CountryField(blank_label='select country', null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s address"

    class Meta:
        verbose_name_plural  = "Addresses"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_seller = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=70, null=True, blank=False)
    price = models.FloatField(null=True, blank=False)
    details = models.CharField(max_length=200, null=True, blank=False)
    available = models.BooleanField(default=True, null=True, blank=False) #sold or not (restock also)
    category = models.CharField(max_length=20, null=True, blank=False, choices=categories)
    req_date = models.DateTimeField(null=True, blank=False, auto_now_add=True)#date when the product is requested to be uploaded by seller
    pub_date = models.DateTimeField(null=True, blank=False, auto_now_add=True)#date when product is uploaded by us after being verified
    image = models.ImageField(upload_to='products/%Y/%m/%d/', default="products/defaultbook.svg", null=True, blank=True)
    condition = models.CharField(max_length=200, null=True, blank=False, choices=conditions)
    amt_sold = models.IntegerField(default=0)
    amt_available = models.IntegerField(null=True, blank=False, default=1)
    paid = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    re_evaluating = models.BooleanField(default=False)
    restocking = models.BooleanField(default=False) #if the seller restocked product
    edited = models.BooleanField(default=False) #if the seller edited a product
    #Customer.product_set.all() to get all products of

    def __str__(self):
        return self.name

    def seller(self):
        return self.seller.user.username

    def total(self):
        return self.amt_available + self.amt_sold

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Product` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Product` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.product.product_seller.__str__() + "'s " + "'{}'".format(self.product.name) + " secondary image."

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

@receiver(models.signals.post_delete, sender=ProductImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ProductImages` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "'s Cart"


class OrderItem(models.Model): #each item which emulates a cart item
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, null=True, blank=False, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, null=True, blank=False, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name

    def total(self):
        return self.quantity * self.product.price

    def items_left(self):
        return self.product.amt_available - self.quantity


class SingleBuy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, null=True, blank=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.product.name + " (single buy)"

    def total(self):
        return self.quantity * self.product.price


class Order(models.Model): #emulates cart cashout
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    sellers = models.ManyToManyField(Customer)
    items = models.ManyToManyField(OrderItem)
    singleitems = models.ManyToManyField(SingleBuy)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=False)

    def __str__(self):
        return "Order by " + self.user.username + " at " + str(self.order_date.strftime("%d/%m/%Y %H:%M:%S"))

class SoldItem(models.Model):
    seller = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=False)
    name = models.CharField(max_length=200, null=True, blank=False)
    details = models.CharField(max_length=200, null=True, blank=True)
    price = models.FloatField(null=True, blank=False)
    quantity = models.IntegerField(default=0)
    products_left = models.IntegerField(default=0)
    purchased_date = models.DateTimeField(auto_now_add=True, null=True, blank=False)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return "Sold " + self.name

    def total(self):
        return self.price * self.quantity

    def p_date(self):
        return str(self.purchased_date.strftime("%d/%m/%Y"))

    def p_time(self):
        return str(self.purchased_date.strftime("%H:%M"))

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

@receiver(models.signals.post_delete, sender=SoldItem)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `SoldItem` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
