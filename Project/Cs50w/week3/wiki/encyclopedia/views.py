from ast import Try, arg
import imp
from sys import argv
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import os


# Create your views here.
def index(request):
    return render(request, "wiki/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)
    return render(request, "wiki/entry.html", {
            "entry": entry,
            "content": content
        })
        
def edit(request, entry):
    path = util.get_path()
    if request.method == "GET":
        print(entry)
        with open(f"{path}\{entry}.md", "r") as file:
            content = file.read()
        return render(request, "wiki/edit.html",{
            "entry": entry,
            "content": content
        })
    else:
        content = request.POST.get("content_name")
        title = request.POST.get("title")

        # validate form
        if not content or not title:
            return render(request, "wiki/edit.html",{
            "entry": entry,
            "content": content,
            "error": "All field are required"
        })
        # rewrite the content
        with open(f"{path}\{entry}.md", "w") as file:
            file.write(content)

        # rewrite the title
        try:
            os.rename(f"{path}\{entry}.md", f"{path}\{title}.md")
        except FileExistsError:
            return render(request, "wiki/edit.html",{
            "entry": title,
            "content": content,
            "error": "This title have already exit"
        })
        return HttpResponseRedirect(reverse("wiki:entry", args=[title]))


