from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Listing, Comment, Bid, Watchlist

class New_listing(forms.Form):
    title = forms.CharField(
        widget = forms.TextInput(attrs = {'placeholder': 'Title'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs = {'placeholder' : 'Enter a description here'}))
    starting_bid = forms.IntegerField()
    image_url = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs = {'placeholder': 'Image URL'}))
    category = forms.ChoiceField(choices = Listing.categories)

class Add_comment_form(forms.Form):
    comment = forms.CharField(label=False)
    
class Add_bid_form(forms.Form):
    bid = forms.IntegerField(label=False)

    
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
        
    else:
        return render(request, "auctions/register.html")

@login_required
def new_listing(request):
    if request.method == "POST":
        form = New_listing(request.POST, 'utf8')      
        if form.is_valid():
            if form.cleaned_data['image_url'] == '':
                form.cleaned_data['image_url'] = 'https://archive.org/download/no-photo-available/no-photo-available.png'
            listing = Listing(
                title = form.cleaned_data["title"],
                description = form.cleaned_data['description'],
                starting_bid = form.cleaned_data['starting_bid'],
                image_url = form.cleaned_data['image_url'],
                category = form.cleaned_data['category'],
                user = request.user)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/new_listing.html", {
        "form": New_listing()
    })

def listing(request, listing_id):
    if request.user.is_authenticated and Watchlist.objects.filter(user=request.user, listing=listing_id).exists():
        on_watchlist = True
    else: 
        on_watchlist = False
        
    if Bid.objects.filter(listing=listing_id).exists():
        highest_bid = Bid.objects.filter(listing=listing_id).latest('bid')
        winner = highest_bid.user
    else:
        highest_bid = 0
        winner = None

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "comments": Comment.objects.filter(listing=listing_id),
        "highest_bid": highest_bid,
        "winner": winner,
        "on_watchlist": on_watchlist,
        "add_comment_form": Add_comment_form(),
        "add_bid_form": Add_bid_form()
    })

@login_required
def add_comment(request, listing_id):
    if request.method == "POST":
        form = Add_comment_form(request.POST, 'utf8')
        if form.is_valid():
            comment = Comment(
                listing = Listing.objects.get(pk=listing_id),
                user = User.objects.get(pk=request.user.id),
                comment = form.cleaned_data["comment"]
            )
            comment.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
@login_required
def add_bid(request, listing_id):
    if request.method == "POST":

        current_price = Listing.objects.get(pk=listing_id).current_price
        starting_bid = Listing.objects.get(pk=listing_id).starting_bid

        form = Add_bid_form(request.POST, 'utf8')
        if form.is_valid():
            bid = Bid(
                listing = Listing.objects.get(pk=listing_id),
                user = User.objects.get(pk=request.user.id),
                bid = form.cleaned_data["bid"]
            )
            if form.cleaned_data["bid"] > current_price and form.cleaned_data["bid"] > starting_bid:
                listing = Listing.objects.get(pk=listing_id)
                listing.current_price = form.cleaned_data["bid"]
                listing.save()     
                bid.save()             
            else:
                messages.add_message(request, messages.INFO, "Your bid must exceed the current highest bid!")  
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def close_auction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        listing.closed = True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.categories   
    })

def category(request, category):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=category)
    })

@login_required
def watchlist(request, listing_id=None):
    if request.method == "POST": 
        user_watchlist = Watchlist.objects.get_or_create(user=request.user)
        user_watchlist = Watchlist.objects.get(user=request.user)

        if Watchlist.objects.filter(user=request.user, listing=listing_id).exists():
            user_watchlist.listing.remove(listing_id)
        else:
            user_watchlist.listing.add(listing_id)    

        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    elif Watchlist.objects.filter(user=request.user).exists():
        return render(request, "auctions/watchlist.html", {
            "watchlist": Watchlist.objects.get(user=request.user).listing.all()
        })
    else:
            return render(request, "auctions/watchlist.html", {
            "watchlist": None
        })