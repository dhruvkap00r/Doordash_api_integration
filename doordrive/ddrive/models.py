from django.db import models
#pickup location is restaurant and dropoff is user's house.
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
  def create_user(self, username, password=None, **extra_fields):
    if not username:
        raise ValueError('Users must have an email address')

    user = self.model(
      username = username
    )

    user.set_password(password)
    user.save(using=self._db)
    return user
  def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
        raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get('is_superuser') is not True:
        raise ValueError("Superuser must have is_superuser=True.")
    return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser):
   
  last_login = None
  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  address = models.TextField()
  phone_number = models.CharField(max_length=15, unique=True)
  username = models.CharField(max_length=100, unique=True)
  password = models.CharField(max_length=100)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  REQUIRED_FIELDS = ['password']
  USERNAME_FIELD = 'username'

class Restaurant_info(models.Model):
  business_name = models.CharField(max_length=20)
  address = models.TextField()
  phone_number = models.CharField(max_length=15)
  email = models.CharField(max_length=100)
  store_id = models.CharField(max_length=30)
  

class Dasher(models.Model):
  dasher_id = models.CharField(max_length=10, unique=True)
  name = models.CharField(max_length=20)
  pickup_phone_number = models.CharField(max_length=15)
  dropoff_phone_number = models.CharField(max_length=15)
  vehicle_make = models.CharField(max_length=100)
  vehicle_model = models.CharField(max_length=100)
  vehicle_year = models.PositiveBigIntegerField()

class DeliveryInfo(models.Model):
  delivery_id = models.CharField(max_length=10)
  is_active = models.BooleanField(default=False)
  is_completed = models.BooleanField(default=False)
  refrence_tag = models.TextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  

  
  
  
  

  