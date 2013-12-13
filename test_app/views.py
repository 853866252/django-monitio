# Create your views here.
from django.views.generic import TemplateView


class TestView(TemplateView):
    template_name = 'test_app/index.html'

class TestFoundationView(TemplateView):
    template_name = 'test_app/foundation_index.html'