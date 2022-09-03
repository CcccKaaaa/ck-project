from django.shortcuts import render

# Create your views here.
def index(request, entry):
    return render(request, "error/index.html", {
        "entry": entry
    })