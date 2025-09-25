from django.urls import path
from django.views.generic import *
from . import views

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("home/<param>/", views.HomeView.as_view(), name="home"),

    path("produits/", views.ProduitListView.as_view(), name="produits"),
    path("produit/<pk>/",views.ProduitDetailView.as_view(), name="detail_produit"),
    path("produit/",views.ProduitCreateView.as_view(), name="creer_produit"),
    path("produit/<pk>/update/",views.ProduitUpdateView.as_view(), name="change_produit"),
    path("produit/<pk>/delete/",views.ProduitDeleteView.as_view(), name="delete_produit"),

    path("categories/", views.CategListView.as_view(), name="categories"),
    path("categorie/<pk>/",views.CategDetailView.as_view(), name="detail_categ"),
    path("categorie/",views.CategCreateView.as_view(), name="creer_categorie"),
    path("categorie/<pk>/update/",views.CategUpdateView.as_view(), name="change_categorie"),
    path("categorie/<pk>/delete/",views.CategDeleteView.as_view(), name="delete_categorie"),

    path("rayons/", views.RayonListView.as_view(), name="rayons"),
    path("rayon/<pk>/",views.RayonDetailView.as_view(), name="detail_rayon"),
    path("rayon/",views.RayonCreateView.as_view(), name="creer_rayon"),
    path("rayon/<pk>/update/",views.RayonUpdateView.as_view(), name="change_rayon"),
    path("rayon/<pk>/delete/",views.RayonDeleteView.as_view(), name="delete_rayon"),

    path("status/", views.StatusListView.as_view(), name="status"),
    path("statut/<pk>/",views.StatusDetailView.as_view(), name="detail_statut"),
    path("statut/",views.StatusCreateView.as_view(), name="creer_statut"),
    path("statut/<pk>/update/",views.StatusUpdateView.as_view(), name="change_statut"),
    path("statut/<pk>/delete/",views.StatusDeleteView.as_view(), name="delete_statut"),

    path("contact_us/", views.ContactView, name="contact_us"),
    path('email_sent/', views.EmailSentView.as_view(), name="email-sent"),
    path("about_us/", views.AboutView.as_view(), name="about_us"),

    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),
]