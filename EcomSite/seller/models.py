from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class HomeAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=200, null=True, blank=False)
    address_line2 = models.CharField(max_length=200, null=True, blank=False) #post office
    state = models.CharField(max_length=200, null=True, blank=False)
    zip_code = models.CharField(max_length=200, null=True, blank=False)
    country = models.CharField(max_length=200, null=True, blank=False)

    def __str__(self):
        return self.user.username + "'s home address"

    class Meta:
        verbose_name_plural  = "Addresses"
