from django.db import models


class CustomCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
