from django.contrib.auth.models import AbstractUser
from django.db import models

    
class User(AbstractUser):
    pass

class Listing(models.Model):
    categories = (
        ("Cats", "Cats"),
        ("Dogs", "Dogs"),
        ("Horses", "Horses"),
    )
    
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
    starting_bid = models.IntegerField(default=0)
    current_price = models.IntegerField(default=0)
    image_url = models.CharField(max_length=64, blank=True)
    category = models.CharField(max_length=16, choices=categories)
    closed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing')

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bid')
    bid = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bid}"
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    comment = models.CharField(max_length=64, default='')

    def __str__(self):
        return f"{self.comment}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    listing = models.ManyToManyField(Listing, null=True, related_name="listing")

    def __str__(self):
        return f"Watchlist - {self.user}"
    
