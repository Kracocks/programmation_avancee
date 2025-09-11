from django.shortcuts import render
from django.http import HttpResponse
from .models import Produit, Categorie, Status

def home(request, param="World"):
    string =request.GET["name"]
    return HttpResponse(f"""<h1>Hello {param}!</h1>
                        <p>{string}</p>""")

def contact_us(request):
    return HttpResponse("""<h1>Contact Us</h1>
                            <p>contact us</p>""")

def about_us(request):
    return HttpResponse("""<h1>About Us</h1>
                            <p>about us</p>""")

def listProduits(request):
    prdts = Produit.objects.all()
    res = "<ul>"
    for prdt in prdts:
        res += f"<li>{prdt}</li>"
    res += "</ul>"

    return HttpResponse(res)

def listCategories(request):
    categories = Categorie.objects.all()
    res = "<ul>"
    for categorie in categories:
        res += f"<li>{categorie}</li>"
    res += "</ul>"

    return HttpResponse(res)

def listStatus(request):
    status = Status.objects.all()
    res = "<ul>"
    for statut in status:
        res += f"<li>{statut}</li>"
    res += "</ul>"

    return HttpResponse(res)