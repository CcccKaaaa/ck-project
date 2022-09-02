from django.shortcuts import render
from encyclopedia import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from re import findall

# globle variable for search result
# Create your views here.
def index(request):
    # get the value of the element name="q" (search field)
    q = request.GET.get("q")
    if q == None:
        return render(request, "search/index.html")
    results = []
    for x in util.list_entries():
        if q.lower() == x.lower():
            return HttpResponseRedirect(reverse("wiki:entry", args=[x]))
        result = findall(f"{q.lower()}", x.lower())
        if result:
            results.append(x)
    return render(request, "search/index.html", {
        "q": q,
        "results": results
    })  