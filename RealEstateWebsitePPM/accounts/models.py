from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.dispatch import receiver
from django.db.models.signals import pre_delete

import os


def user_image_directory_path(instance, filename):
    print(instance.username)
    folder_name = f"user_{instance.username}"
    return os.path.join('users', folder_name, filename)


class CustomUser(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(message='Please enter a valid email address.')], unique=True, blank=False, null=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    profile_picture = models.ImageField(upload_to=user_image_directory_path, blank=True, null=True)

    def __str__(self):
        return self.username

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()


@receiver(pre_delete, sender=CustomUser)
def delete_user(sender, instance, **kwargs):
    # Delete associated image
    if instance.profile_picture:
        image_path = instance.profile_picture.path
        instance.profile_picture.delete()
        if os.path.exists(image_path):
            os.remove(image_path)

        directory_path = os.path.dirname(image_path)
        try:
            os.removedirs(directory_path)
        except OSError:
            pass
