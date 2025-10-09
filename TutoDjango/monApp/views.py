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
from .models import Produit, Categorie, Status, Rayon, Contenir
from .forms import ContactUsForm, ProduitForm, CategForm, RayonForm, StatusForm, ContenirForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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

    def get_queryset(self):
        # Charge les catégories et les statuts en même temps
        query = self.request.GET.get('search')
        if query:
            return Produit.objects.filter(intituleProd__icontains=query).select_related('categorie').select_related('status')
        return Produit.objects.select_related('categorie').select_related('status')

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

@method_decorator(login_required, name="dispatch")
class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/create_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('detail_produit', prdt.refProd)

@method_decorator(login_required, name="dispatch")
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/update_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('detail_produit', prdt.refProd)

@method_decorator(login_required, name="dispatch")
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
        query = self.request.GET.get('search')
        if query:
            return Categorie.objects.filter(nomCat__icontains=query).annotate(nb_produits=Count('produits'))
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
        context['produits'] = self.object.produits.all()
        return context

@method_decorator(login_required, name="dispatch")
class CategCreateView(CreateView):
    model = Produit
    form_class=CategForm
    template_name = "monApp/create_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        categ = form.save()
        return redirect('detail_categ', categ.idCat)

@method_decorator(login_required, name="dispatch")
class CategUpdateView(UpdateView):
    model = Categorie
    form_class=CategForm
    template_name = "monApp/update_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        categ = form.save()
        return redirect('detail_categ', categ.idCat)

@method_decorator(login_required, name="dispatch")
class CategDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/delete_categorie.html"
    success_url = reverse_lazy('categories')

# Pages Rayon
class RayonListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rayons"

    def get_queryset(self):
        # Précharge tous les "contenir" de chaque rayon,
        # et en même temps le produit de chaque contenir
        query = self.request.GET.get('search')
        if query:
            return Rayon.objects.filter(nomRayon__icontains=query).prefetch_related(
                Prefetch("rayons", queryset=Contenir.objects.select_related("produits"))
            )
        return Rayon.objects.prefetch_related(
            Prefetch("rayons", queryset=Contenir.objects.select_related("produits"))
        )

    def get_context_data(self, **kwargs):
        context = super(RayonListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        rayons_data = []
        for rayon in context['rayons']:
            total = 0
            for contenir in rayon.rayons.all():
                total += contenir.produits.prixUnitaireProd * contenir.quantite
            rayons_data.append({'rayon': rayon,'total_stock': total})
        context['rayons_data'] = rayons_data
        return context

class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "rayon"

    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        produits_data = []
        total_rayon = 0
        total_nb_produit = 0

        for contenir in self.object.rayons.all():
            total_produit = contenir.produits.prixUnitaireProd * contenir.quantite
            produits_data.append({ 'contenir': contenir,
                                   'produit': contenir.produits,
                                   'qte': contenir.quantite,
                                   'prix_unitaire': contenir.produits.prixUnitaireProd,
                                   'total_produit': total_produit})
            total_rayon += total_produit
            total_nb_produit += contenir.quantite

        context['produits_data'] = produits_data
        context['total_rayon'] = total_rayon
        context['total_nb_produit'] = total_nb_produit
        return context

@method_decorator(login_required, name="dispatch")
class RayonCreateView(CreateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/create_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('detail_rayon', rayon.idRayon)

@method_decorator(login_required, name="dispatch")
class RayonUpdateView(UpdateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/update_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('detail_rayon', rayon.idRayon)

@method_decorator(login_required, name="dispatch")
class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/delete_rayon.html"
    success_url = reverse_lazy('rayons')

# Pages Status
class StatusListView(ListView):
    model = Status
    template_name = "monApp/list_status.html"
    context_object_name = "status"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        query = self.request.GET.get('search')
        if query:
            return Status.objects.filter(libelle__icontains=query).annotate(nb_produits=Count('produits'))
        return Status.objects.annotate(nb_produits=Count('produits'))

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
        context['produits'] = self.object.produits.all()
        return context

@method_decorator(login_required, name="dispatch")
class StatusCreateView(CreateView):
    model = Status
    form_class=StatusForm
    template_name = "monApp/create_status.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        statut = form.save()
        return redirect('detail_statut', statut.identifiant)

@method_decorator(login_required, name="dispatch")
class StatusUpdateView(UpdateView):
    model = Status
    form_class=StatusForm
    template_name = "monApp/update_statut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        statut = form.save()
        return redirect('detail_statut', statut.identifiant)

@method_decorator(login_required, name="dispatch")
class StatusDeleteView(DeleteView):
    model = Status
    template_name = "monApp/delete_statut.html"
    success_url = reverse_lazy('status')

# Create
@method_decorator(login_required, name="dispatch")
class ContenirCreateView(CreateView):
    model = Contenir
    form_class=ContenirForm
    template_name = "monApp/create_contenir.html"

    def get_context_data(self, **kwargs):
        context = super(ContenirCreateView, self).get_context_data(**kwargs)
        context['rayon'] = self.kwargs.get("pk")
        return context

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = Rayon.objects.get(pk=self.kwargs['pk'])
        produit = form.cleaned_data['produits']
        quantite = form.cleaned_data['quantite']

        contenir_existe = Contenir.objects.filter(rayons=rayon, produits=produit).first()

        if contenir_existe:
            contenir_existe.quantite += quantite
            contenir_existe.save()
        else:
            contenir = form.save(commit=False)
            contenir.rayons = rayon
            contenir.save()
        return redirect('detail_rayon', rayon.idRayon)

@method_decorator(login_required, name='dispatch')
class ContenirUpdateView(UpdateView):
    model = Contenir
    form_class = ContenirForm
    template_name = "monApp/update_contenir.html"
    pk_url_kwarg = 'pk_c'

    def form_valid(self, form):
        contenir = form.save(commit=False)

        if contenir.quantite <= 0:
            contenir.delete()
        else:
            contenir.save()

        return redirect('detail_rayon', contenir.rayons.idRayon)


@method_decorator(login_required, name='dispatch')
class ContenirDeleteView(DeleteView):
    model = Contenir
    template_name = "monApp/delete_contenir.html"
    pk_url_kwarg = 'pk_c'

    def get_success_url(self):
        rayon = self.object.rayons
        return reverse_lazy('detail_rayon', args=[rayon.idRayon])

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
