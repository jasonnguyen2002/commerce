from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Bid, Comments, Category, Watchlist
import datetime

def index(request):
    now = datetime.datetime.now()
    if Listing.objects.all().exists:
        return render(request, "auctions/index.html",{
            "listings": Listing.objects.all(),
            "current_date": now
        })

def create_listing(request):
    if request.method == "GET":
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {
            "categories": categories
        })
    if request.method == "POST":
        title = request.POST.get('title')
        image = request.FILES.get('image')
        date = request.POST.get('date')
        price = request.POST.get('price')
        category = request.POST.get('category')
        description = request.POST.get('description')

        new_category = Category.objects.get(category=category)
        if not Listing.objects.filter(listing_title=title).exists():
            new_listing = Listing.objects.create(
            listing_title=title,
            listing_imageurl=image,
            listing_author = request.user,
            listing_datecreate = datetime.datetime.now(),
            listing_activeuntil = date,
            listing_setPrice=price,
            listing_highestBidder=request.user,
            listing_category=new_category,
            listing_description=description
            )
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Auction already exists!"
            })
    return render(request, "auctions/create_listing.html")

def watchlist(request):
    user_watchlist = Watchlist.objects.get(user=request.user)
    user= User.objects.get(id=request.user)
    return render(request, "auctions/watchlist.html",{
        "listing": user_watchlist.product.all(),
        "user": user
    })

def listing_page(request, title):
    listing = Listing.objects.get(listing_title=title)
    if request.method == "POST":
        if 'watchlist' in request.POST:
            if Watchlist.objects.filter(user=request.user).exists():
                user_watchlist = Watchlist.objects.get(user=request.user)
                if not user_watchlist.product.filter(id=listing.id).exists():
                    user_watchlist.product.add(listing)
                    user_watchlist.save()
                    return render(request, "auctions/listing_page.html", {
                        "TITLE": title,
                        "listing": listing,
                        "commnets": Comments.objects.filter(product_name=listing),
                        "message": f"{listing.listing_title} has been added to your watchlist!"
                    })
                else:
                    return render(request, "auctions/listing_page.html", {
                        "listing": listing,
                        "TITLE": title,
                        "commnets": Comments.objects.filter(product_name=listing),
                        "message": f"{listing.listing_title} is already on your watchlist."
                    })
            else:
                new_user = Watchlist(user=request.user)
                new_user.save()
                new_user.product.add(listing)
                return render(request, "auctions/listing_page.html", {
                    "TITLE": title,
                    "message": f"{listing.listing_title} has been added to your watchlist!"
                })
        elif "bid" in request.POST:
            if request.user != listing.listing_author:
                new_bid = Bid.objects.create(bid_listing=listing, bid_option=request.POST.get("bid"), bid_by=request.user)
                new_bid.save()
                if new_bid.bid_option > listing.listing_setPrice:
                    listing.objects.update(listing_setPrice=new_bid.bid_option, listing_highestBidder=request.user)
                return render(request, "auctions/listing_page.html", {
                    "listing": listing,
                    "TITLE": title,
                    "commnets": Comments.objects.filter(product_name=listing),
                    "message": "Bid added!"
                })
            else:
                return render(request, "auctions/listing_page.html", {
                    "listing": listing,
                    "TITLE": title,
                    "comments": Comments.objects.filter(product_name=listing),
                    "message": "The original author cannot bid on their own auction!"
                })
        elif "comments" in request.POST:
            if request.user.is_authenticated:
                new_comment = Comments.objects.create(user=request.user, comment=request.POST.get("commnets"), product_name=listing)
                new_comment.save()
            else:
                return render(request, "auctions/listing_page.html", {
                    "listing": listing,
                    "TITLE": title,
                    "commnets": Comments.objects.filter(product_name=listing),
                    "message": "You must log in to make a comment"
                })

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "TITLE": title,
        "comments": Comments.objects.filter(product_name=listing)
    })

def categories(request, category):
    all_listings = Listing.objects.filter(listing_category=category)
    return render(request, "auctions/catgory.html", {
        "listing": all_listings,
        "category": category
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
    

    
    
