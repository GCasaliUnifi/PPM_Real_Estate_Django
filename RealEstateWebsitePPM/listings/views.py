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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        # Sorting
        sort_param = self.request.GET.get('sort')
        sorting_options = {
            'price': 'price',
            'bedrooms': 'bedrooms',
            'bathrooms': 'bathrooms',
            'squaremt': 'square_metres',
        }

        if sort_param in sorting_options:
            sort_field = sorting_options[sort_param]
            queryset = queryset.order_by(sort_field)

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
        # Process the form submission and send the message to the seller
        # Add any necessary logic here

        # Show a success message
        messages.success(request, "Your message has been sent successfully!")

        # Redirect to a thank-you page or another appropriate page
        return redirect('success_page')
