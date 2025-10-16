from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.views import ContenirCreateView, ContenirUpdateView, ContenirDeleteView
from monApp.models import Contenir, Rayon, Produit

class CategorieUrlsTest(TestCase):
    def setUp(self):
        self.produit = Produit.objects.create(intituleProd="prod", prixUnitaireProd=59.99, dateFabricationProd='2025-09-09')
        self.rayon = Rayon.objects.create(nomRayon="rayon")
        self.contenir = Contenir.objects.create(produits=self.produit, rayons=self.rayon, quantite=60)
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
    
    # Test URL
    def test_contenir_create_url_is_resolved(self): # Test URL créer
        url = reverse('cntnr_crt', args=[self.rayon.pk])
        self.assertEqual(resolve(url).view_name, 'cntnr_crt')
        self.assertEqual(resolve(url).func.view_class, ContenirCreateView)

    def test_contenir_update_url_is_resolved(self): # Test URL change
        url = reverse('cntnr_upt', args=[self.rayon.pk, self.contenir.pk])
        self.assertEqual(resolve(url).view_name, 'cntnr_upt')
        self.assertEqual(resolve(url).func.view_class, ContenirUpdateView)

    def test_contenir_delete_url_is_resolved(self): # Test URL suppréssion
        url = reverse('cntnr_dlt', args=[1, 1])
        self.assertEqual(resolve(url).view_name, 'cntnr_dlt')
        self.assertEqual(resolve(url).func.view_class, ContenirDeleteView)
    
    # Test code d'erreur (OK = code bon, KO = pas bon)
    def test_contenir_create_response_code_OK(self):
        response = self.client.get(reverse('cntnr_crt', args=[self.rayon.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_contenir_update_response_code_OK(self):
        url = reverse('cntnr_upt', args=[self.rayon.pk, self.contenir.pk]) # id existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_contenir_update_response_code_KO(self):
        url = reverse('cntnr_upt', args=[self.rayon.pk, 9999]) # id non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_contenir_delete_response_code_OK(self):
        url = reverse('cntnr_dlt', args=[self.rayon.pk, self.contenir.pk]) # id existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_contenir_delete_response_code_KO(self):
        url = reverse('cntnr_dlt', args=[self.rayon.pk, 9999]) # id non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # Test redirection
    def test_redirect_after_contenir_creation(self):
        response = self.client.post(reverse('cntnr_crt', args=[self.rayon.pk]), {'produits': self.produit.pk, 'quantite': 60})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f"/monApp/rayon/{self.rayon.idRayon}/")

    def test_redirect_after_contenir_updating(self):
        response = self.client.post(reverse('cntnr_upt', args=[self.rayon.pk, self.contenir.pk]),
                                    data={'produits': self.produit.pk, 'quantite': 50})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f"/monApp/rayon/{self.rayon.idRayon}/")

    def test_redirect_after_contenir_deletion(self):
        response = self.client.post(reverse('cntnr_dlt', args=[self.rayon.pk, self.contenir.pk]))
        # Vérifie qu'on a bien une redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/monApp/rayon/{self.rayon.idRayon}/")
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Contenir.objects.filter(pk=self.contenir.pk).exists())