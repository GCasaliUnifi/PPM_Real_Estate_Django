from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

import os

# Create your views here.
from django.conf import settings
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from listings.models import Listing


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        redirect_to = self.request.POST.get('next')
        if redirect_to:
            return redirect_to
        else:
            return reverse_lazy('home')


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs.get('pk')
        user_listings = Listing.objects.filter(owner=user_pk)[:3]
        context['user_listings'] = user_listings
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "registration/profile_edit.html"

    def get_success_url(self):
        return reverse_lazy("profile_details", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        # Retrieve old user profile_picture
        print("Retrieve old pfp")
        old_profile_picture = self.object.profile_picture
        if old_profile_picture:
            print("old_pfp exists: " + old_profile_picture.path + "  --- nome: " + old_profile_picture.name)

        # Controlla se una nuova immagine è stata caricata
        if 'profile_picture' in form.changed_data:
            new_profile_picture = form.cleaned_data['profile_picture']
            self.object.profile_picture = new_profile_picture

        # Add debugging statements
        print("Form is valid. Saving user profile.")

        # Save the form and user profile
        response = super().form_valid(form)

        # Add debugging statements
        print("User profile saved successfully.")

        return response

    def form_invalid(self, form):
        #  debugging statements
        print("Form is invalid.")

        # Display form validation errors as messages
        messages.error(self.request, "Please correct the errors in the form.")

        return super().form_invalid(form)


# Contact Profile View is different from the Contact Seller View because it is not associated with a listing
class ContactProfileView(LoginRequiredMixin, TemplateView):
    template_name = "contact_profile.html"
    success_url = reverse_lazy("success_page")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_pk = self.kwargs.get('pk')
        contacted_user = get_object_or_404(CustomUser, pk=user_pk)
        context['contacted_user_pk'] = user_pk
        context['contacted_user'] = contacted_user.username
        return context

    def post(self, request, *args, **kwargs):
        # Process the form submission and send the message to the seller
        # Add any necessary logic here

        # Show a success message
        messages.success(request, "Your message has been sent successfully!")

        # Redirect to a thank-you page or another appropriate page
        return redirect('home')
