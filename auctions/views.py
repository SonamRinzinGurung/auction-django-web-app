import datetime
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    category_id = request.GET.get('category')
    listings = AuctionListing.objects.filter(flActive=True)
    for listing in listings:
        if request.user in listing.watchers.all():
            listing.is_watched = True
        else:
            listing.is_watched = False
    
    return render(request, "auctions/index.html",{
        "listings": listings,
        'title': 'Active Auctions'
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


ListingForm = forms.modelform_factory(AuctionListing, fields=('title', 'description', 'start_bid','category', 'image'))


@login_required
def createListing(request):
    
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            start_bid = form.cleaned_data['start_bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            creator = request.user
            auction = AuctionListing(title=title,description=description,
                                     start_bid=start_bid,image=image,category=category,
                                     creator=creator,datetime=datetime.datetime.now())
            auction.save()
            return render(request,"auctions/create.html",{
                "form":ListingForm,
                "success":True
            })
        else:
            return render(request,"auctions/create.html",{
                "form": ListingForm,
            })
    return render(request, "auctions/create.html",{
        "form": ListingForm
    })
    
    
BidForm = forms.modelform_factory(Bids, fields=('bid',))

CommentForm = forms.modelform_factory(Comment, fields=('comment',),widgets = {
            'comment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Leave your comment here',
        })
    })
    
    
def listing(request, listing_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.user in listing.watchers.all():
        listing.is_watched = True
    else:
        listing.is_watched = False
    
    return render(request, "auctions/listing.html",{
        "listing": listing,
        'bidform': BidForm,
        "comments": listing.comment.all(),
        'commentform': CommentForm
    })
    
    


@login_required
def take_bid(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    offer = float(request.POST['bid'])
    
    if offer >= listing.start_bid and (listing.current_bid is None or offer > listing.current_bid):
        listing.current_bid = offer
        form = BidForm(request.POST)
        newBid = form.save(commit=False)
        newBid.auction = listing
        newBid.user = request.user
        newBid.save()
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "bidform": BidForm,
            "error_bid": True,
            "commentform": CommentForm,
        })
        
        
@login_required
def comment(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    form = CommentForm(request.POST)
    newComment = form.save(commit=False)
    newComment.auction = listing
    newComment.user = request.user
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            
            
def close_listing(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    
    if request.user == listing.creator:
        listing.flActive = False
        listing.buyer = Bids.objects.filter(auction=listing).last().user
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    
    
@login_required
def watchlist(request):
    listings = request.user.watched_listing.all()
    
    for listing in listings:
        if request.user in listing.watchers.all():
            listing.is_watched = True
        else:
            listing.is_watched = False
    return render(request, "auctions/index.html", {
        'listings': listings,
        'title': 'My Watchlist'
        
    })


def toggle_watchlist(request, listing_id, reverse_method):
    listings = AuctionListing.objects.get(pk=listing_id)
    if request.user in listings.watchers.all():
        listings.watchers.remove(request.user)
    else:
        listings.watchers.add(request.user)
        
    if reverse_method == 'listing':
        return listing(request, listing_id)
    else:
        return HttpResponseRedirect(reverse(reverse_method))
    
    
def category(request):

    categories = Category.objects.all()
    
    return render(request, "auctions/category.html", {
        'categories': categories,
    })
    

def category_listing(request, category_id):
    listings = AuctionListing.objects.filter(category=category_id)
    return render(request, "auctions/category_listings.html", {
        'listings': listings,
        'title': 'Category Listings'
        })