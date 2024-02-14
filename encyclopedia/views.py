from django.http import HttpResponse
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "entry": entry
    })

