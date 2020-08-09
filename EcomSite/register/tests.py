from django.test import TestCase
from store.models import Customer
from django.contrib.auth.models import User
# Create your tests here.

class CreateUserTest(TestCase):

    def test_create_user(self):
        user = User(first_name='Mike', last_name='Johnson', email='mj@gmail.com',
                    username='mjforever', password="now12345")

        return Customer(user=user)
