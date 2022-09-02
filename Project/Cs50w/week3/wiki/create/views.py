from django.shortcuts import render
from encyclopedia import util
from django.urls import reverse
from django.http import HttpResponseRedirect
from encyclopedia import util

# Create your views here.
def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content_name")
        for x in util.list_entries():
            if x.lower() == title.lower():
                return render(request, "create/index.html", {
                    "title": title,
                    "content": content,
                    "error": "The title have already exit"
                })
        path = util.get_path()        
        with open(f"{path}\{title}.md", "a") as file:
            file.write(content)
        return HttpResponseRedirect(reverse("wiki:entry", args=[title]))
    else:
        return render(request, "create/index.html") 