import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

genders = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('NS', 'Prefer not to say'),
        ('OT', 'Other')
]

class Profile(models.Model):
    sellerid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=False)
    gender = models.CharField(max_length=20, null=True, blank=False, choices=genders)
    citizenship = models.CharField(max_length=20, null=True, blank=False)

    def __str__(self):
        return self.user.username + "'s profile"

    def age(self):
        return datetime.datetime.now() - self.date_of_birth

    def full_name(self):
        return self.user.get_full_name()

    def first_name(self):
        return self.user.get_short_name()


class HomeAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, null=True, blank=False, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=200, null=True, blank=False)
    address_line2 = models.CharField(max_length=200, null=True, blank=False) #post office
    city = models.CharField(max_length=200, null=True, blank=False)
    state = models.CharField(max_length=200, null=True, blank=False)
    zip_code = models.CharField(max_length=200, null=True, blank=False)
    country = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return self.user.username + "'s home address"

    class Meta:
        verbose_name_plural  = "Addresses"
