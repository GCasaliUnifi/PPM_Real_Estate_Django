from django.views.generic import TemplateView
from listings.models import Listing


class HomePageView(TemplateView):
    template_name = "home.html"

    # TODO limit the number of featured listings to 6
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["featured_listings"] = Listing.objects.filter(is_featured=True)
        return context


class SuccessPageView(TemplateView):
    template_name = "operation_success.html"
