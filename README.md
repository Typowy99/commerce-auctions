# Commerce Project - Django Auction Site
This is a simple e-commerce auction site created as Project 2 for CS50’s Web Programming with Python. The project is built with Python, Django, and HTML/CSS. The goal is to allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a "watchlist."

## Overview
The application consists of four main models: User, AuctionListing, Bid, Category and Comment. Each model is designed to capture relevant information for the auction site.

## Features
- ** Create Listing ** - Users can visit a page to create a new auction listing. They can specify a title, a text-based description, and the starting bid. Optional fields include a URL for an image and a category (e.g., Fashion, Toys, Electronics).

- ** Active Listings Page ** - The default route of the web application lets users view all currently active auction listings. For each active listing, this page displays the title, description, current price, and photo (if one exists for the listing).

- ** Listing Page ** - Clicking on a listing takes users to a page specific to that listing. On that page, users can view all details about the listing, including the current price for the listing.

    - If the user is signed in, they can add the item to their "Watchlist." If the item is already on the watchlist, the user can remove it.
    - If the user is signed in, they can bid on the item. The bid must be at least as large as the starting bid and greater than any other bids that have been placed.
    - If the user is signed in and is the one who created the listing, they have the ability to "close" the auction from this page, making the highest bidder the winner of the auction and making the listing no longer active.
    - If a user is signed in on a closed listing page and has won that auction, the page will say so.
    - Users who are signed in can add comments to the listing page, and the listing page displays all comments that have been made on the listing.

- ** Watchlist ** - Users who are signed in can visit a Watchlist page, which displays all the listings that a user has added to their watchlist. Clicking on any of those listings takes the user to that listing’s page.

- ** Categories ** - Users can visit a page that displays a list of all listing categories. Clicking on the name of any category takes the user to a page that displays all the active listings in that category.

- ** Django Admin Interface ** - Via the Django admin interface, a site administrator can view, add, edit, and delete any listings, comments, and bids made on the site.

## Setup
Requires Python3 and the package installer for Python (pip) to run:

1. Install requirements (Django4): pip install -r requirements.txt
2. After cloning the repository, refer to the project folder and:
    - Create new migrations based on the changes in models: python3 manage.py makemigrations
    - Apply the migrations to the database: python3 manage.py migrate
    - Create a superuser to be able to use Django Admin Interface: python3 manage.py createsuperuser
    - Run the app locally: python3 manage.py runserver
3. Visit the site: http://localhost:8000
4. Enjoy!

# Built With
- Python
- Django
- HTML/CSS

# Future Work
Some challenges for future enhancements include making a nicer front-end design.