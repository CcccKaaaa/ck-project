from django.shortcuts import render
import random
from encyclopedia import util
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def random_page(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:entry", args=[entry]))
