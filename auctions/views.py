from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Bid, User, Category, AuctionListing, Comment
from .forms.auction_forms import AuctionListingForm, BidForm

def index(request):
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })



def auction(request, auction_id):
    auction = AuctionListing.objects.get(id=auction_id)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        
        form = BidForm(request.POST, auction=auction)

        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = request.user
            bid.auction = auction
            bid.save()
            
            auction.current_price = bid.price
            auction.save()

            return redirect('auction', auction_id=auction_id)
    else:
        form = BidForm(auction=auction)
    
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "form": form
    })


@login_required(login_url='login')
def watchlist(request, auction_id):
    if request.method == "POST":
        auction = AuctionListing.objects.get(id=auction_id)
        user_watchlists = request.user.watchlist.all()

        if auction in user_watchlists:
            request.user.watchlist.remove(auction)
        else:
            request.user.watchlist.add(auction)

    return redirect('auction', auction_id)


@login_required(login_url='login')
def watchlist_view(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "auctions": watchlist
    })


@login_required(login_url='login')
def create_auction(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            new_auction = form.save(commit=False)
            new_auction.owner_auction = request.user
            new_auction.save()

            return redirect('index')
            
    else:
        form = AuctionListingForm()

    return render(request, "auctions/create_auction.html", {
        "form": form
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
