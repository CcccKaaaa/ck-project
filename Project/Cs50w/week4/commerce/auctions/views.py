from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
        next_url = request.POST.get('next')
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
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
        category = request.POST.get("category")
        if not category:
            category = "other"
        is_listing = True
        user = User.objects.get(pk=request.user.id)
        price = request.POST.get("price")
        a = Auctions(
            title=title,
            description=description, 
            image_url=image_url, 
            is_listing=is_listing, 
            create_by=user, 
            category=category
            )
        a.save()

        b = Bids(bid_by=user, price=price, auctions_bid=a)
        b.save()
        return HttpResponseRedirect(reverse('auctions:listing', args=[str(a.id)]))

    
@login_required(login_url="/login")
def watchlist(request):
    user = request.user
    watchlist = WatchList.objects.filter(watch_by=user.id).values_list("watch_auction", flat=True)
    listings =[]
    for listing in watchlist:
        listing = Auctions.objects.get(pk=listing)
        bids = listing.bid.all()
        current_bid = max(bids, key=lambda x:x.price)
        listing_info = {
            "info": listing,
            "current_bid": current_bid.price
        }
        listings.append(listing_info)
    return render(request, "auctions/watchlist.html" ,{
        "listings": listings
    })


def categories(request):
    return render(request, "auctions/categories.html", {"category_choices":category_choices})

def category(request, category):
    entries = Auctions.objects.filter(category=category, is_listing=1)
    listings =[]
    for listing in entries:
        listing = Auctions.objects.get(pk=listing.id)
        bids = listing.bid.all()
        current_bid = max(bids, key=lambda x:x.price)
        listing_info = {
            "info": listing,
            "current_bid": current_bid.price
        }
        listings.append(listing_info)

    return render(request, "auctions/category.html", {"listings":listings})

def listings(request, auction_id):
    #listing = Auctions.objects.get(pk=auction_id) 
    listing = get_object_or_404(Auctions, pk=auction_id)
    category = listing.category
    bids = listing.bid.all()
    bid_count = len(bids) - 1
    bid_max = max(bids, key=lambda x:x.price)
    bid_start = min(bids, key=lambda x:x.price)
    bid_form = form.bid()
    user = request.user.id
    close_permission = False
    status = "Avaiable"
    winner = None
    comment_form = form.comment()
    comments = Comments.objects.filter(commented_on=auction_id)
    # User can not bid on their own listing but able to close it
    if listing.is_listing == True:
        if user == listing.create_by.id:
            bid_form = None
            close_permission = True
    else:
        bid_form = None
        status = "Closed"
        # define the winner
        # check if have any bid (excep the owner)
        if len(bids) != 1:
            winner = bid_max.bid_by
            if winner.id == user:
                winner = "You have won this listing"
            else:
                winner = winner.username
    # Check if user are watching this listing
    watch_by = WatchList.objects.filter(watch_auction=listing).values_list("watch_by", flat=True)
    if request.user.id in watch_by:
        state = "Watching"
    else:
        state = "Add to Watchlist"
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "category":category,
            "bid_start": bid_start,
            "bid_max": bid_max,
            "bid_count": bid_count, 
            "bid_form": bid_form, 
            "state": state,
            "close_permission": close_permission, 
            "status":status, 
            "winner": winner,
            "comments": comments,
            "comment_form":comment_form
        })
    # Post bid
    else:
        # Check authenticated
        if request.user.is_authenticated:
            # submit bid
            if "bid" in request.POST:
                new_bid = request.POST.get("price")
                # TODO need improve with server side validation
                if int(new_bid) <= bid_max.price:
                    error = "Your bid must greater than the current bid"
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "category":category,
                        "bid_start": bid_start,
                        "bid_max": bid_max,
                        "bid_count": bid_count, 
                        "bid_form": bid_form, 
                        "message": error,
                        "state": state,
                        "close_permission": close_permission,
                        "status":status,
                        "winner": winner,
                        "comments": comments,
                        "comment_form":comment_form
                    })
                b = Bids(bid_by=request.user,auctions_bid=listing, price=new_bid)
                b.save()    
                return HttpResponseRedirect(reverse('auctions:listing', args=[auction_id]))
            # Add to Watchlist
            if "watchlist" in request.POST:
                if state == "Watching":
                    WatchList.objects.get(watch_by=request.user, watch_auction=listing).delete()
                else:
                    watch_by = request.user
                    watch_auction = listing
                    w = WatchList(watch_by=watch_by, watch_auction=watch_auction)
                    w.save()
                return HttpResponseRedirect(reverse('auctions:listing', args=[auction_id]))

            # Close the listing
            if "close" in request.POST:
                # Update database
                listing.is_listing = False
                listing.save()
                return HttpResponseRedirect(reverse('auctions:listing', args=[auction_id]))

            # Post comment
            if "comment" in request.POST:
                    c = Comments(
                        commented_by=request.user, 
                        commented_on=listing,
                        content=request.POST.get("content")
                        )
                    c.save()
                    print(True)
                    return HttpResponseRedirect(reverse("auctions:listing", args=[auction_id]))
        else:
            return HttpResponseRedirect(reverse("auctions:login")+f"?next=/listing/{auction_id}")
