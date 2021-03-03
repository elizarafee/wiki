from django.shortcuts import render
from django import forms
from . import util
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
import random
import markdown2

class SearchForm(forms.Form):
    searchEntry = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class CreateEntryForm(forms.Form):
    entryTitle = forms.CharField(label="Title:", widget=forms.TextInput(attrs={'placeholder': "Title of the entry's page"}))
    markdownContent = forms.CharField(label="Markdown Content:", widget=forms.Textarea(attrs={'placeholder': "Write markdown content for this page...",'style': 'height: 200px;width:500px'}))

class EditEntryForm(forms.Form):
    markdownContent = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': "Write markdown content for this page..." ,'style': 'height: 200px;width:500px'}))

def index(request):                                  
    if request.method == "POST":
        searchForm = SearchForm(request.POST)
        if searchForm.is_valid():
            searchResults = []
            searchEntry = searchForm.cleaned_data["searchEntry"]
            entries = util.list_entries()
            for entry in entries:
                if len(searchEntry)!=len(entry) and searchEntry.lower() in entry.lower():
                    searchResults.append(entry)
            if searchResults:
                return render(request, "encyclopedia/index.html", {
                        "entries": searchResults,
                        "searchForm": searchForm,
                        "searchResults": searchResults
                    }) 
            else:
                return render(request, "encyclopedia/entry.html", {
                    "searchForm": searchForm,
                    "title" : util.get_entry(searchEntry)
                })      
        else:
            return render(request, "encyclopedia/index.html", {
                "searchForm": searchForm
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "searchForm" : SearchForm()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "searchForm" : SearchForm(),
        "title": title,
        "markdown" : markdown2.markdown(util.get_entry(title))
    })

def createEntry(request):
    if request.method == "POST":
        createEntryform = CreateEntryForm(request.POST)
        if createEntryform.is_valid():
            entryTitle = createEntryform.cleaned_data["entryTitle"]
            markdownContent = createEntryform.cleaned_data["markdownContent"]
            entries = util.list_entries()
            for entry in entries:
                if entryTitle.lower() == entry.lower():
                    return HttpResponse("ERROR:: Sorry!!! An entry with this title is already available in the entries, so try with another title!")
           
            return render(request, 'encyclopedia/entry.html', {
                    "searchForm" : SearchForm(),
                    "title": entryTitle,
                    "markdownContent": markdownContent,
                    "save_entry" : util.save_entry(entryTitle, markdownContent)
                })

    return render(request, "encyclopedia/createEntry.html", {
        "searchForm" : SearchForm(),
        "createEntryform": CreateEntryForm()
    })

def editEntry(request, title):
    if request.method == "POST":
        editEntryForm = EditEntryForm(request.POST)
        if editEntryForm.is_valid():
            markdownContent = editEntryForm.cleaned_data["markdownContent"]
            return render(request, 'encyclopedia/entry.html', {
                    "searchForm" : SearchForm(),
                    "title": title,
                    "markdownContent": markdown2.markdown(markdownContent),
                    "save_entry" : util.save_entry(title, markdownContent)
                })
        else:
            return HttpResponse('ERROR:: Sorry! Updating failed..')
    print("PUT didnt got toouch")

    return render(request, "encyclopedia/editEntry.html", {
        "searchForm" : SearchForm(),
        "editEntryForm": EditEntryForm(),
        "title": title
    })

def randomEntry(request):
    entries = util.list_entries()
    randomEntry = random.choice (entries)
    return render(request, 'encyclopedia/entry.html', {
        "searchForm" : SearchForm(),
        "title": randomEntry,
        "markdown" : markdown2.markdown(util.get_entry(randomEntry))
    })