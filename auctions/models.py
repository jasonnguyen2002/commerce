from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username=models.CharField(max_length=12, blank=False, unique=True)
    email=models.EmailField(('email address'), unique=True)
    password=models.CharField(max_length=16, unique=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']
    
class Category(models.Model):
    category = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.category}"



class Listing(models.Model):
    listing_title= models.CharField(max_length=128)
    listing_imageurl = models.FileField(null=True, blank=True, upload_to="listingimages/")
    listing_author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    listing_datecreate=models.DateField(null=True)
    listing_activeuntil=models.DateField(null=True, blank=True)
    listing_setPrice = models.DecimalField(max_digits=8, decimal_places=2)
    listing_highestBidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="bidder")
    listing_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='categories')
    listing_description = models.TextField(null=True)
    
    def __str__(self):
        return f"{self.listing_title}\n{self.listing_author}\n{self.listing_datecreate}\n{self.listing_activeuntil}\n{self.listing_setPrice}\n{self.listing_highestBidder}\n{self.listing_category}\n{self.listing_description}"
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    comment = models.TextField(max_length=1000, null=True, blank=True)
    product_name = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product")

    def __str__(self):
        return f"{self.user}\n{self.comment}\n{self.product_name}"

class Bid(models.Model):
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_option = models.DecimalField(max_digits=8, decimal_places=2)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.product}\n{self.highest_bid}\n"\

class Watchlist(models.Model):
    product = models.ManyToManyField(Listing)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")