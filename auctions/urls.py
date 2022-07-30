from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/<int:listing_id>/bid", views.take_bid, name="take_bid"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment"),
    path("listing/<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/change/<str:reverse_method>", views.toggle_watchlist, name="toggle_watchlist"),
    path("category/", views.category, name="category"),
    path("category/<int:category_id>", views.category_listing, name="category_listing"),
]

