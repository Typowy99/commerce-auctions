from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category_name}"


class AuctionListing(models.Model):
    owner_auction = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    img_url = models.URLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save_current_price(self, *args, **kwargs):
        self.auction.current_price = self.price
        self.auction.save()
        super(Bid, self).save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

