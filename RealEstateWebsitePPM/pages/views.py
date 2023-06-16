from django.views.generic import TemplateView, ListView
from django.db.models import Q
from listings.models import Listing
from accounts.models import CustomUser


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_listings"] = Listing.objects.filter(is_featured=True)
        return context


class SuccessPageView(TemplateView):
    template_name = "operation_success.html"


class SearchView(ListView):
    template_name = "search_template.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_param = self.request.GET.get('search')

        if query_param:
            queryset_listing = Listing.objects.filter(
                Q(title__icontains=query_param) | Q(description__icontains=query_param)
            )

            queryset_users = CustomUser.objects.filter(
                username__icontains=query_param
            )

            context["listings_search"] = queryset_listing
            context["users_search"] = queryset_users

        return context

    def get_queryset(self):
        query_param = self.request.GET.get('search')
        if query_param:
            listings_search = Listing.objects.filter(
                Q(title__icontains=query_param) | Q(description__icontains=query_param)
            )
            users_search = CustomUser.objects.filter(
                username__icontains=query_param
            )

            return listings_search, users_search

        return None, None
