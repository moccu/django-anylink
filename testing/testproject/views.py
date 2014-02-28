from __future__ import unicode_literals
from django.views.generic import ListView

from .models import Linklist


class LinklistView(ListView):
    model = Linklist
    template_name = 'example.html'
