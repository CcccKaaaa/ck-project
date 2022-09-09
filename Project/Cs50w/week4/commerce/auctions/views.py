from email import message
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from auctions import form
from .models import *

def index(request):
    active_listing = Auctions.objects.filter(is_listing=1)
    listings =[]
    for listing in active_listing:
        bids = listing.bid.all()
        current_bid = max(bids, key=lambda x:x.price)

        # merge info of Auctions table and Bids table to display each listing on the page
        listing_info = {
            "info": listing,
            "current_bid": current_bid.price
        }
        listings.append(listing_info)
    return render(request, "auctions/index.html", {"listings":listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            # https://stackoverflow.com/questions/16750464/django-redirect-after-login-not-working-next-not-posting
            
            if next_url:
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="/login")
def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            'form': form.createForm(),
            "bid": form.bid()
        })
    else:
        title = request.POST.get("title")
        description = request.POST.get("description")
        image_url = request.POST.get("image_url")
        is_listing = True
        user = User.objects.get(pk=request.user.id)
        price = request.POST.get("price")
        a = Auctions(
            title=title,
            description=description, 
            image_url=image_url, 
            is_listing=is_listing, 
            create_by=user
            )
        a.save()

        b = Bids(bid_by=user, price=price, auctions_bid=a)
        b.save()
        return HttpResponseRedirect(reverse('auctions:listing', args=[str(a.id)]))

    
@login_required(login_url="/login")
def watchlist(request):
    return render(request, "auctions/register.html")
def categories(request):
    return render(request, "auctions/register.html")


def listing(request, auction_id):
    listing = Auctions.objects.get(pk=auction_id)
    bids = listing.bid.all()
    bid_count = len(bids)
    bid_max = max(bids, key=lambda x:x.price)
    bid_start = min(bids, key=lambda x:x.price)
    bid_form = form.bid()
    user = request.user.id
    # User can not bid on their own listing
    if user == listing.create_by.id:
        bid_form = None

    # Check if user are watching this listing
    watch_by = WatchList.objects.filter(watch_auction=listing).values_list("watch_by", flat=True)
    if request.user.id in watch_by:
        state = "Watching"
    else:
        state = "Add to Watchlist"
    print(request.user.id)
    print(watch_by)
    print(state)
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "bid_start": bid_start,
            "bid_max": bid_max,
            "bid_count": bid_count, 
            "bid_form": bid_form, 
            "state": state
        })

    # Post bid
    else:
        # submit bid
        print(request.POST)
        if "bid" in request.POST:
            new_bid = request.POST.get("price")
            if int(new_bid) <= bid_max.price:
                error = "Your bid must greater than the current bid"
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bid_start": bid_start,
                    "bid_max": bid_max,
                    "bid_count": bid_count, 
                    "bid_form": bid_form, 
                    "message": error,
                    "state": state
                })
            b = Bids(bid_by=request.user,auctions_bid=listing, price=new_bid)
            b.save()
            return HttpResponseRedirect(reverse('auctions:listing', args=[auction_id]))
        # Add to Watchlist
        if "watchlist" in request.POST:
            if state == "Watching":
                print(state, 1)
                WatchList.objects.get(watch_by=request.user, watch_auction=listing).delete()
            else:
                print(state, 2)
                watch_by = request.user
                watch_auction = listing
                w = WatchList(watch_by=watch_by, watch_auction=watch_auction)
                w.save()
            return HttpResponseRedirect(reverse('auctions:listing', args=[auction_id]))
        print("error")
        return HttpResponseRedirect(reverse('auctions:listing', args=[auction_id]))