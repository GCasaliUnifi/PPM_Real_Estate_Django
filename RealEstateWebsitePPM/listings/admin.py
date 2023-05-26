from django.contrib import admin

# Register your models here.

from .models import Category
from .models import Listing


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


admin.site.register(Category, CategoryAdmin)


class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "square_feet", "list_date", "owner", "is_published")


admin.site.register(Listing, ListingAdmin)
