from django.urls import path

from .views import (
    PropertyListView,
    PropertyCreateView,
    PropertyDetailView,
    PropertyDeleteView,
    ContactSellerView,
)

urlpatterns = [
    path("<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),
    path("<int:pk>/contact_seller/", ContactSellerView.as_view(), name="contact_seller"),
    path("<int:pk>/delete/", PropertyDeleteView.as_view(), name="property_delete"),
    path("new/", PropertyCreateView.as_view(), name="listing_create"),
    path("", PropertyListView.as_view(), name="property_list"),
]
