from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse


class SearchForm(forms.Form):
    searchEntry = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def index(request):                                      #"wiki/" + str(searchEntry))) #("{% url 'wiki/{}'.format(searchEntry) %}"))
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            searchResults = []
            searchEntry = form.cleaned_data["searchEntry"]
            entries = util.list_entries()
            for entry in entries:
                if len(searchEntry)!=len(entry) and searchEntry.lower() in entry.lower():
                    searchResults.append(entry)
            if searchResults:
                return render(request, "encyclopedia/index.html", {
                        "entries": searchResults,
                        "form": form,
                        "searchResults": searchResults
                    }) 
            else:
                return render(request, "encyclopedia/entry.html", {
                    "form": form,
                    "title" : util.get_entry(searchEntry)
                })      
        else:
            return render(request, "encyclopedia/index.html", {
                "form": form
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form" : SearchForm()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "form" : SearchForm(),
        "title" : util.get_entry(title)
    })

def search(request):
    return render(request, "encyclopedia/entry.html", {
        "searchEntry" : searchEntry
    })