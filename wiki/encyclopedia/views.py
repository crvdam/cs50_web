from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from django import forms
import random
import markdown2


from . import util

class CreateForm(forms.Form):
    title = forms.CharField(
        widget = forms.TextInput(attrs = {'placeholder': 'Title'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs = {'placeholder' : 'Your text here'}))

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):    
    if entry not in util.list_entries():
        raise Http404
    
    return render(request, "encyclopedia/entry.html", {
    "title": entry,
    "entry": markdown2.markdown(util.get_entry(entry))
    })

def search(request):
    query = request.POST['q']
    if query in util.list_entries():
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=(query,)))
    
    results = [s for s in util.list_entries() if query.lower() in s.lower()]    

    return render(request, "encyclopedia/search.html", { 
        "results": results
    })

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST, 'utf8')      
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"].encode()              
            if title in util.list_entries():
                error = "That title already exists."
                return render(request, "encyclopedia/create.html", {
                    "error": error,
                    "form": form
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))           
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, 'encyclopedia/create.html', {
        "form": CreateForm()
    })

def edit(request, entry):
    form = EditForm(request.POST)
    if request.method == "POST":
        form = EditForm(request.POST)
        
        if form.is_valid():
            content = form.cleaned_data["content"].encode()
            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(entry,)))
    
    form = EditForm()
    form.fields['content'].initial = util.get_entry(entry)
    return render(request, "encyclopedia/edit.html", {
        "title": entry,
        "form": form
    })

def randomentry(request):
    list =  util.list_entries()
    random_entry = random.randint(0, len(list) - 1)
    return HttpResponseRedirect(reverse("encyclopedia:entry", args=(list[random_entry],)))       




    
        
