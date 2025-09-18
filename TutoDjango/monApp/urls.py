from django.urls import path
from django.views.generic import *
from . import views

urlpatterns = [
    path("home", views.HomeView.as_view()),
    path("home/<param>", views.HomeView.as_view()),
    path("produits", views.ProduitListView.as_view(), name="produits"),
    path("produit/<pk>/",views.ProduitDetailView.as_view(), name="detail_produit"),
    path("categories", views.CategListView.as_view(), name="categories"),
    path("categorie/<pk>/",views.CategDetailView.as_view(), name="detail_categ"),
    path("rayons", views.RayonListView.as_view(), name="rayons"),
    path("rayon/<pk>/",views.RayonDetailView.as_view(), name="detail_rayon"),
    path("status", views.StatusListView.as_view(), name="status"),
    path("statut/<pk>/",views.StatusDetailView.as_view(), name="detail_statut"),
    path("contact_us", views.ContactView.as_view(), name="contact_us"),
    path("about_us", views.AboutView.as_view(), name="about_us"),
]