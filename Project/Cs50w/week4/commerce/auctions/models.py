from django.contrib.auth.models import AbstractUser
from django.db import models

category_choices = [
    ("property_rent","Property for rent"),
    ("vehicles","Vehicles"),
    ("classifieds","Classifieds"),
    ("clothing","Clothing"),
   ("electronics","Electronics"),
    ("entertainment","Entertainment"),
    ("family","Family"),
    ("free","Free stuff"),
    ("garden","Garden and outdoors"),
    ("hobbies","Hobbies"),
    ("home_goods","Home goods"),
    ("home_supplies","Home improvement supplies"),
    ("instruments","Musical instruments"),
    ("office","Office supplies"),
    ("pet_supplies","Pet supplies"),
    ("property_sell","Property for sale"),
    ("sporting","Sporting goods"),
    ("toys","Toys & games"),
    ("other","Other"),
    ]

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass
   
# Autions
class Auctions(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, null=True)
    is_listing = models.BooleanField()
    category = models.CharField(max_length=100, null=True,blank=True, choices=category_choices)
    image_url = models.CharField(max_length=256, blank=True, null=True, default="https://demofree.sirv.com/nope-not-here.jpg")

    create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created")
    
    def __str__(self):
        return f"{self.id}: Create by {self.create_by} with title {self.title}"

# Bids
class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding")
    auctions_bid = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="bid")
    price = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.id}: bid by {self.bid_by} in {self.auctions_bid} with price {self.price}"

# Comment
class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented")
    commented_on = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return f"{self.commented_by} on {self.commented_on}"

# Watch list
class WatchList(models.Model):
    id = models.AutoField(primary_key=True)
    watch_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")
    watch_auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="inlist")
    
    def __str__(self):
        return f"{self.watch_auction} in watchlist of {self.watch_by}"
