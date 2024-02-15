from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util

class NewEntryForm(forms.Form):
    new_title = forms.CharField(label="New Title", widget=forms.TextInput(attrs={'size':'40'}))
    new_entry = forms.CharField(label="", widget=forms.Textarea(attrs={'style':'width: 60%; height: 50vh'}))

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

    # if there is a match, display the entry page
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

# entry display view for the title
def new_page(request):

    # POST: when form is submitted - process saving new entry function
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['new_title']
            new_entry = form.cleaned_data['new_entry']
            
            # check if new title already exists in the DB
            entries = util.list_entries()
            for entry in entries:
                if new_title.lower() == entry.lower():
                    error = "Error: Entry title already in the database. Please try again."
                    return render(request, "encyclopedia/new_page.html", {
                        "error": error,
                        "form": NewEntryForm()
                    })
            
            # everything looks good - save and display the new entry page
            util.save_entry(new_title, new_entry)
            return wiki(request, new_title)
    
    # GET: display an empty form
    return render(request, "encyclopedia/new_page.html", {
        "form": NewEntryForm()
    })
