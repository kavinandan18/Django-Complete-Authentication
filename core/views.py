from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create HomePageViews here.
class HomePageView(TemplateView):
    template_name = 'core/index.html'


