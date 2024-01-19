from django.contrib import admin
from .models import Bid, User, Category, AuctionListing, Comment
# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("id", "owner_auction", "title", "price", "category", "created_at", "is_active")
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Comment)