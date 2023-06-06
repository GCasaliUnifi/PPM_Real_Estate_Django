from django.db import models
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import pre_delete
import uuid
import os

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


def listing_image_directory_path(instance, filename):
    # Generate a UUID for the listing
    listing_uuid = uuid.uuid4().hex
    # Create a unique folder name using the UUID and the listing's ID
    folder_name = f"listing_{instance.owner}_{listing_uuid}"
    # Upload image to a directory named after the unique folder name
    return os.path.join('listings', folder_name, filename)


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    square_metres = models.PositiveIntegerField()
    # TODO add location field
    listing_location = models.CharField(max_length=200)
    image = models.ImageField(upload_to=listing_image_directory_path, blank=True, null=True)
    is_published = models.BooleanField()
    is_featured = models.BooleanField(default=False)
    list_date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("property_detail", kwargs={"pk": self.pk})


@receiver(pre_delete, sender=Listing)
def delete_listing(sender, instance, **kwargs):
    # Delete associated image
    if instance.image:
        image_path = instance.image.path
        instance.image.delete()
        if os.path.exists(image_path):
            os.remove(image_path)

        directory_path = os.path.dirname(image_path)
        try:
            os.removedirs(directory_path)
        except OSError:
            pass
