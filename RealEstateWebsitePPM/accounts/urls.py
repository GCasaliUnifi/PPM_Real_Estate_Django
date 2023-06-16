from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import SignUpView, ProfileView, EditProfileView, ContactProfileView, CustomLoginView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/<int:pk>/edit", EditProfileView.as_view(), name="profile_edit"),
    path("profile/<int:pk>/contact_profile", ContactProfileView.as_view(), name="contact_profile"),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile_details"),
]
