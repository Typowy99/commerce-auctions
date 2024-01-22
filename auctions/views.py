from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Bid, User, Category, AuctionListing, Comment
from .forms.auction_forms import AuctionListingForm, BidForm, CommentForm


def index(request):
    auctions = AuctionListing.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "categories": categories
    })


def auction(request, auction_id):
    try:
        auction = AuctionListing.objects.get(id=auction_id)
    except AuctionListing.DoesNotExist:
        raise Http404("Aukcja nie istnieje")
    
    comments = Comment.objects.filter(auction=auction).order_by('-created_at')
    categories = Category.objects.all()

    user_watchlist = False
    owner_auction = False
    if request.user.is_authenticated:
        user_watchlist_auctions = request.user.watchlist.all()
        if auction in user_watchlist_auctions:
            user_watchlist = True

        if request.user == auction.owner_auction:
            owner_auction = True

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
        "form": form,
        "form_note": CommentForm(),
        "comments": comments,
        "user_watchlist": user_watchlist,
        "owner_auction": owner_auction,
        "categories": categories
    })


def category(request, category_name):
    category = Category.objects.get(category_name=category_name)
    auctions = AuctionListing.objects.filter(category=category, is_active=True).order_by('-created_at')
    categories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "categories": categories,
        "category": category
    })


@login_required(login_url='login')
def add_comment(request, auction_id):
    auction = AuctionListing.objects.get(id=auction_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']
            comment = Comment.objects.create(user=request.user, comment_text=comment_text, auction=auction)
            auction.comments.add(comment)
            auction.save()

            return redirect(request.META['HTTP_REFERER'])
    else:
        form = CommentForm()

    return render(request, 'add_note.html', {'form': form})


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
    categories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "auctions": watchlist,
        "categories": categories
    })


@login_required(login_url='login')
def create_auction(request):
    categories = Category.objects.all()
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
        "form": form,
        "categories": categories
    })


@login_required(login_url='login')
def close_auction(request, auction_id):
    auction = get_object_or_404(AuctionListing, id=auction_id)

    if auction.owner_auction == request.user and auction.is_active:
        auction.close_auction()

        return redirect('auction', auction_id)
    else:
        return render(request, 'auctions/error.html', {
            "message": "You are not allowed to close this auction."
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

