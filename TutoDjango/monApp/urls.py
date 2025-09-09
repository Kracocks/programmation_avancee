from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("home/<param>", views.home, name="home"),
    path("produits", views.listProduits, name="produits"),
    path("categories", views.listCategories, name="categories"),
    path("status", views.listStatus, name="status"),
    path("contact_us", views.contact_us, name="contact_us"),
    path("about_us", views.about_us, name="about_us"),
]