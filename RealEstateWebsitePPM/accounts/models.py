from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(message='Please enter a valid email address.')], unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
