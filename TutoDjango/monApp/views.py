from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Produit, Categorie, Status, Rayon

def home(request):
    if request.GET and request.GET["test"]:
        raise Http404
    return HttpResponse("Bonjour Monde!")

def contact_us(request):
    return render(request, 'monApp/contact.html')

def about_us(request):
    return render(request, 'monApp/about.html')

def listProduits(request):
    prdts = Produit.objects.all()
    return render(request, 'monApp/list_produits.html', {'produits': prdts})

def listCategories(request):
    categories = Categorie.objects.all()
    return render(request, 'monApp/list_categories.html', {'categs': categories})

def listStatus(request):
    status = Status.objects.all()
    return render(request, 'monApp/list_status.html', {'status': status})

def listRayons(request):
    rayons = Rayon.objects.all()
    return render(request, 'monApp/list_rayons.html', {'rayons': rayons})