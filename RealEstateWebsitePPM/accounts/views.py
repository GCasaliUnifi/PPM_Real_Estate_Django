from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView

# Create your views here.

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# TODO ricorda di aggiungere il LoginRequiredMixin a tutte le classi
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileView(DetailView):
    model = CustomUser
    template_name = "profile_details.html"


class EditProfileView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "registration/profile_edit.html"

    def get_success_url(self):
        return reverse_lazy("profile_details", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
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
