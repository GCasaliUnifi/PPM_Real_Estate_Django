from django.urls import path
from .views import HomePageView, SuccessPageView, SearchView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("success/", SuccessPageView.as_view(), name="success_page"),
    path("search/", SearchView.as_view(), name="search")
]
