from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.views import ProduitListView, ProduitDetailView, ProduitCreateView, ProduitUpdateView, ProduitDeleteView
from monApp.models import Produit

class CategorieUrlsTest(TestCase):
    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="ProduitPourTest", prixUnitaireProd=59.99, dateFabricationProd="2025-09-09")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
    
    # Test URL
    def test_produit_list_url_is_resolved(self):
        url = reverse('produits')
        self.assertEqual(resolve(url).view_name, 'produits')
        self.assertEqual(resolve(url).func.view_class, ProduitListView)

    def test_produit_detail_url_is_resolved(self):
        url = reverse('detail_produit', args=[1])
        self.assertEqual(resolve(url).view_name, 'detail_produit')
        self.assertEqual(resolve(url).func.view_class, ProduitDetailView)

    def test_produit_create_url_is_resolved(self):
        url = reverse('creer_produit')
        self.assertEqual(resolve(url).view_name, 'creer_produit')
        self.assertEqual(resolve(url).func.view_class, ProduitCreateView)

    def test_produit_update_url_is_resolved(self):
        url = reverse('change_produit', args=[1])
        self.assertEqual(resolve(url).view_name, 'change_produit')
        self.assertEqual(resolve(url).func.view_class, ProduitUpdateView)

    def test_produit_delete_url_is_resolved(self):
        url = reverse('delete_produit', args=[1])
        self.assertEqual(resolve(url).view_name, 'delete_produit')
        self.assertEqual(resolve(url).func.view_class, ProduitDeleteView)
    
    # Test code d'erreur
    def test_produit_list_response_code(self):
        response = self.client.get(reverse('produits'))
        self.assertEqual(response.status_code, 200)
    
    def test_produit_detail_response_code(self):
        url = reverse('detail_produit', args=[self.produit.refProd]) #refProd existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_produit_detail_response_code_KO(self):
        url = reverse('detail_produit', args=[9999]) # refProd non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_produit_create_response_code_OK(self):
        response = self.client.get(reverse('creer_produit'))
        self.assertEqual(response.status_code, 200)
    
    def test_produit_update_response_code_OK(self):
        url = reverse('change_produit', args=[self.produit.refProd]) # refProd existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_produit_update_response_code_KO(self):
        url = reverse('change_produit', args=[9999]) # refProd non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_produit_delete_response_code_OK(self):
        url = reverse('delete_produit', args=[self.produit.refProd]) # refProd existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_produit_delete_response_code_KO(self):
        url = reverse('delete_produit', args=[9999]) # refProd non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # Test redirection
    def test_redirect_after_produit_creation(self):
        response = self.client.post(reverse('creer_produit'), {'intituleProd': 'ProduitPourTestRedirectionCreation', 'prixUnitaireProd': '59.99', 'dateFabricationProd': '2025-09-09'} )
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, '/monApp/produit/2/')

    def test_redirect_after_produit_updating(self):
        response = self.client.post(reverse('change_produit', args=[self.produit.refProd]),
        data={"intituleProd": "ProduitPourTestRedirectionMaj", 'prixUnitaireProd': '59.99', 'dateFabricationProd': '2025-09-09'})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f'/monApp/produit/{self.produit.refProd}/')

    def test_redirect_after_produit_deletion(self):
        response = self.client.post(reverse('delete_produit', args=[self.produit.pk]))
        # Vérifie qu'on a bien une redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('produits'))
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Produit.objects.filter(pk=self.produit.pk).exists())