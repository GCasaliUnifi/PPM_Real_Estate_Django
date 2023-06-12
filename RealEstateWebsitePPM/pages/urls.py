from django.urls import path
from .views import HomePageView, SuccessPageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("success/", SuccessPageView.as_view(), name="success_page"),
]
