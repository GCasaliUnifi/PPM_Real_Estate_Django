from django.db import models
from django.conf import settings
from django.urls import reverse
import uuid, os

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


def listing_image_directory_path(instance, filename):
    # Generate a unique filename for the image (uuid)
    listing_uuid = uuid.uuid4().hex
    # Upload to a directory named after the listing uuid
    return os.path.join('listings', listing_uuid, filename)


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    square_feet = models.PositiveIntegerField()
    # TODO add location field
    listing_location = models.CharField(max_length=200)
    image = models.ImageField(upload_to="listing_image_directory_path", blank=True, null=True)
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
