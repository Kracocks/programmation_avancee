from django.db.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import *
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import BaseModelForm
from django.urls import reverse_lazy
from .models import Produit, Categorie, Status, Rayon
from .forms import ContactUsForm, ProduitForm, CategForm, RayonForm, StatusForm

class HomeView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        param = self.kwargs.get('param', 'DJANGO')
        context['titreh1'] = f"Hello {param}"
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)

class AboutView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)

def ContactView(request):
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via TutoDjango Contact form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monApp.com'],    
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()
    titreh1 = "Contact us !"
    return render(request, "monApp/page_home.html", {'titreh1':titreh1, 'form':form})

class EmailSentView(TemplateView):
    template_name = "monApp/page_email_sent.html"

    def get_context_data(self, **kwargs):
        context = super(EmailSentView, self).get_context_data(**kwargs)
        context['titreh1'] = "Votre mail à été envoyé !"
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)

# Pages Produit
class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "produits"

    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context

class ProduitDetailView(DetailView):
    model = Produit
    template_name = "monApp/detail_produit.html"
    context_object_name = "produit"

    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context

class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/create_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('detail_produit', prdt.refProd)

class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/update_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('detail_produit', prdt.refProd)

class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = "monApp/delete_produit.html"
    success_url = reverse_lazy('produits')

# Pages Categorie
class CategListView(ListView):
    model = Categorie
    template_name = "monApp/list_categories.html"
    context_object_name = "categs"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits'))

    def get_context_data(self, **kwargs):
        context = super(CategListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context

class CategDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "categ"

    def get_context_data(self, **kwargs):
        context = super(CategDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        return context

class CategCreateView(CreateView):
    model = Produit
    form_class=CategForm
    template_name = "monApp/create_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        categ = form.save()
        return redirect('detail_categ', categ.idCat)

class CategUpdateView(UpdateView):
    model = Categorie
    form_class=CategForm
    template_name = "monApp/update_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        categ = form.save()
        return redirect('detail_categ', categ.idCat)

class CategDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/delete_categorie.html"
    success_url = reverse_lazy('categories')

# Pages Rayon
class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rayons"

    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        return context

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "rayon"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        return context

class RayonCreateView(CreateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/create_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('detail_rayon', rayon.idRayon)

class RayonUpdateView(UpdateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/update_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('detail_rayon', rayon.idRayon)

class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/delete_rayon.html"
    success_url = reverse_lazy('rayons')

# Pages Status
class StatusListView(ListView):
    model = Status
    template_name = "monApp/list_status.html"
    context_object_name = "status"

    def get_context_data(self, **kwargs):
        context = super(StatusListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes status"
        return context

class StatusDetailView(DetailView):
    model = Status
    template_name = "monApp/detail_statut.html"
    context_object_name = "statut"

    def get_context_data(self, **kwargs):
        context = super(StatusDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        return context

class StatusCreateView(CreateView):
    model = Status
    form_class=StatusForm
    template_name = "monApp/create_status.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        statut = form.save()
        return redirect('detail_status', statut.identifiant)

class StatusUpdateView(UpdateView):
    model = Status
    form_class=StatusForm
    template_name = "monApp/update_status.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        statut = form.save()
        return redirect('detail_status', statut.identifiant)

class StatusDeleteView(DeleteView):
    model = Status
    template_name = "monApp/delete_status.html"
    success_url = reverse_lazy('status')

# Page Login
class ConnectView(LoginView):
    template_name = 'monApp/page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monApp/page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'monApp/page_register.html')

class RegisterView(TemplateView):
    template_name = 'monApp/page_register.html'

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monApp/page_login.html')
        else:
            return render(request, 'monApp/page_register.html')

class DisconnectView(TemplateView):
    template_name = 'monApp/page_logout.html'

    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
