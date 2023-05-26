from django.urls import path

from .views import (
    PropertyListView,
    PropertyCreateView,
    PropertyDetailView,
)

urlpatterns = [
    path("<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),
    path("new/", PropertyCreateView.as_view(), name="listing_create"),
    path("", PropertyListView.as_view(), name="property_list"),
]
