import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
#from store.models import Customer
# Create your models here.

genders = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NS', 'Prefer not to say'),
        ('OT', 'Other')
]

tiers = [
        ('T1', 'Tier 1'),
        ('T2', 'Tier 2'),
        ('T3', 'Tier 3'),
]

class Profile(models.Model):
    sellerid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=False)
    gender = models.CharField(max_length=20, null=True, blank=False, choices=genders)
    phone = models.CharField(max_length=20, null=True, blank=False)
    email = models.CharField(max_length=200, null=True, blank=False)
    business = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profilepics/%Y/%m/%d/', null=True, blank=True)
    note = models.CharField(max_length=200, null=True, blank=False)
    vouches = models.ManyToManyField('store.Customer')
    tier = models.CharField(max_length=50, null=True, blank=False, choices=tiers)

    def __str__(self):
        return self.user.username + "'s profile"

    def age(self):
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

        return '{} years'.format(age)

    def full_name(self):
        return self.user.get_full_name()

    def first_name(self):
        return self.user.get_short_name()

    def vouches_amt(self):
        return self.vouches.all().count()

    @property
    def imageURL(self):
        try:
            url = self.profile_pic.url
        except:
            url = ''
        return url

class HomeAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=200, null=True, blank=False)
    address_line2 = models.CharField(max_length=200, null=True, blank=False) #post office
    city = models.CharField(max_length=200, null=True, blank=False)
    state = models.CharField(max_length=200, null=True, blank=False)
    zip_code = models.CharField(max_length=200, null=True, blank=False)
    country = CountryField(blank_label='select country', null=True, blank=True)

    def __str__(self):
        return self.user.username + "'s home address"

    class Meta:
        verbose_name_plural  = "Addresses"


class Pickup(models.Model):
    user = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=True, blank=False)
    date = models.DateField(null=True, blank=False)
    time = models.TimeField(null=True, blank=False)
    phone = models.CharField(max_length=11, null=True, blank=False)

    def __str__(self):
        return self.user.username + "'s " + str(self.date) + " pickup"
