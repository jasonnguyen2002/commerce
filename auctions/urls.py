from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("<str:title>/", views.listing_page, name="listing_page"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("<str:category>.", views.categories, name="categories"),
]
