from django.views.generic import ListView

from .models import Linklist


class LinklistView(ListView):
    model = Linklist
    template_name = 'example.html'
