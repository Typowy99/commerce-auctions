from django import forms
from ..models import Bid, AuctionListing

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'price', 'img_url', 'category']

    def clean_price(self):
        """
        Custom validation for the price field.
        Ensures that the price is not negative.
        """
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
    

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['price']

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
