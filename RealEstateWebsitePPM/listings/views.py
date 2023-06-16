import urllib.parse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, TemplateView
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import Category, Listing


class PropertyListView(ListView):
    model = Listing
    template_name = "property_list.html"

    sort_mapping = {
        "1": "Price (low to high)",
        "2": "Price (high to low)",
        "3": "Date Posted (newest first)",
        "4": "Date Posted (oldest first)",
        "5": "Square metres (low to high)",
        "6": "Square metres (high to low)",
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sort_param = self.request.GET.get('sort')
        if sort_param:
            sort_name = self.sort_mapping.get(sort_param, "")
            if sort_name:
                context["sort_name"] = sort_name
            else:
                context["sort_name"] = "None"
        else:
            context["sort_name"] = "None"
        context["categories"] = Category.custom_objects.all()

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtering
        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)

        l_location = self.request.GET.get('location')
        if l_location:
            # TODO: Add function to handle location filtering and also split the location into city and address
            pass

        date_posted = self.request.GET.get('date_posted')
        if date_posted:
            queryset = queryset.filter(list_date=date_posted)

        min_square_metres = self.request.GET.get('min_sqm')
        if min_square_metres:
            queryset = queryset.filter(square_metres__gte=min_square_metres)

        min_bedrooms = self.request.GET.get('min_bedrooms')
        if min_bedrooms:
            queryset = queryset.filter(bedrooms__gte=min_bedrooms)

        min_bathrooms = self.request.GET.get('min_bathrooms')
        if min_bathrooms:
            queryset = queryset.filter(bathrooms__gte=min_bathrooms)

        # Sorting
        sort_param = self.request.GET.get('sort')
        sort_map = {
            "1": "price",
            "2": "-price",
            "3": "-list_date",
            "4": "list_date",
            "5": "square_metres",
            "6": "-square_metres",
        }

        if sort_param:
            orderby_param = sort_map.get(sort_param, "")
            if orderby_param:
                queryset = queryset.order_by(orderby_param)

        return queryset


class MyPropertyListView(LoginRequiredMixin, ListView):
    model = Listing
    template_name = "property_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.filter(owner=user)
        return queryset


class PropertyDetailView(DetailView):
    model = Listing
    template_name = "property_detail.html"


class PropertyCreateView(CreateView):
    model = Listing
    template_name = "listing_create.html"
    success_url = reverse_lazy("home")
    fields = (
        "title",
        "description",
        "listing_location",
        "bedrooms",
        "bathrooms",
        "square_metres",
        "price",
        "image",
        "category",
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.custom_objects.all()
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.list_date = timezone.now()
        form.instance.is_published = True
        return super().form_valid(form)


class PropertyDeleteView(DeleteView):
    model = Listing
    # TODO change this to redirect to the user's listings
    success_url = reverse_lazy("home")


class ContactSellerView(LoginRequiredMixin, TemplateView):
    template_name = "contact_seller.html"
    success_url = reverse_lazy("success_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        listing_pk = self.kwargs.get('pk')
        listing = get_object_or_404(Listing, pk=listing_pk)
        context['listing_title'] = listing.title
        context['listing_pk'] = listing_pk
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request, "Your message has been sent successfully!")
        return redirect('success_page')
