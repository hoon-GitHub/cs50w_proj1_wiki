from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# entry display view for the title
def wiki(request, title):
    entry = util.get_entry(title)
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "entry": entry
    })

# search view
def search(request):
    keyword = request.GET.get("q", "")
    entry = util.get_entry(keyword)

    # if there is a match
    if not entry == None:
        return wiki(request, keyword)
    
    # if there is not a match, check if there is any substring match(es)
    else:
        matches = []
        for match in util.list_entries():
            if keyword.lower() in match.lower():
                matches.append(match)
            
        return render(request, "encyclopedia/search.html", {
            "keyword": keyword,
            "matches": matches
        })
