from asyncio.windows_events import NULL
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.category}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(null=True, max_length=1024)
    start_bid = models.FloatField()
    current_bid = models.FloatField(null=True,blank=True)
    flActive = models.BooleanField(default=True)
    image = models.CharField(max_length=2083)
    datetime = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="similar_listing")
    creator = models.ForeignKey(User,default=NULL,on_delete=models.CASCADE, related_name="all_creators_listing")
    watchers = models.ManyToManyField(User,blank=True, related_name="watched_listing")
    buyer = models.ForeignKey(User,null=True,blank=True,on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.title}: Start Bid: {self.start_bid}"
    
    
class Bids(models.Model):
    auction = models.ForeignKey(AuctionListing,on_delete=models.CASCADE, related_name="auction")
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="bidder")
    bid = models.FloatField()
    date = models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return f"{self.user.username} bid {self.bid} on {self.auction.title}"
    

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="commenter")
    auction = models.ForeignKey(AuctionListing,on_delete=models.CASCADE, related_name="comment")
    comment = models.CharField(max_length=200)
    createdDate = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.createdDate.strftime("%Y-%m-%d %H:%M:%S")