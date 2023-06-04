from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

# Create your views here.

from .forms import CustomUserCreationForm
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
    # fields = ['first_name', 'last_name', 'phone_number', 'date_of_birth', 'address']
    fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'address']
    template_name = "registration/profile_edit.html"
    success_url = reverse_lazy("profile_details")
