from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_auction", views.create_auction, name="create_auction"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("watchlist/<int:auction_id>", views.watchlist, name="watchlist"),
    path("watchlist_view", views.watchlist_view, name="watchlist_view")
]
