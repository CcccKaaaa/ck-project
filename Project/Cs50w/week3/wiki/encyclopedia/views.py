
from ast import arg
from django.shortcuts import render
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
import os
from markdown2 import Markdown


# Create your views here.
def index(request):
    return render(request, "wiki/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    for x in util.list_entries():
        if entry.lower() == x.lower():
            content = util.get_entry(entry)
            markdowner = Markdown()
            content= markdowner.convert(content)
            return render(request, "wiki/entry.html", {
                    "entry": entry,
                    "content": content
                })
    return HttpResponseRedirect(reverse("error:index", args=[entry]))
        
def edit(request, entry):
    path = util.get_path()
    if request.method == "GET":
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
        # https://www.pythontutorial.net/python-basics/python-read-text-file/
        # https://copyprogramming.com/howto/python-writelines-newline
        # https://www.geeksforgeeks.org/python-string-splitlines-method/
        # rewrite the content
        with open(f"{path}\{entry}.md", "w") as file:
            content = content.splitlines()
            print(f"content before write \n {content}")
            file.writelines(f"{line}\n" for line in content)
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

