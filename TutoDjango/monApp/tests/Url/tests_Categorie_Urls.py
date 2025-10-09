from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from monApp.views import CategListView, CategDetailView, CategCreateView, CategUpdateView, CategDeleteView
from monApp.models import Categorie

class CategorieUrlsTest(TestCase):
    def setUp(self):
        self.categ = Categorie.objects.create(nomCat="CategoriePourTest")
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
    
    # Test URL
    def test_categorie_list_url_is_resolved(self):
        url = reverse('categories')
        self.assertEqual(resolve(url).view_name, 'categories')
        self.assertEqual(resolve(url).func.view_class, CategListView)

    def test_categorie_detail_url_is_resolved(self):
        url = reverse('detail_categ', args=[1])
        self.assertEqual(resolve(url).view_name, 'detail_categ')
        self.assertEqual(resolve(url).func.view_class, CategDetailView)

    def test_categorie_create_url_is_resolved(self):
        url = reverse('creer_categorie')
        self.assertEqual(resolve(url).view_name, 'creer_categorie')
        self.assertEqual(resolve(url).func.view_class, CategCreateView)

    def test_categorie_update_url_is_resolved(self):
        url = reverse('change_categorie', args=[1])
        self.assertEqual(resolve(url).view_name, 'change_categorie')
        self.assertEqual(resolve(url).func.view_class, CategUpdateView)

    def test_categorie_delete_url_is_resolved(self):
        url = reverse('delete_categorie', args=[1])
        self.assertEqual(resolve(url).view_name, 'delete_categorie')
        self.assertEqual(resolve(url).func.view_class, CategDeleteView)
    
    # Test code d'erreur
    def test_categorie_list_response_code(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, 200)
    
    def test_categorie_detail_response_code(self):
        url = reverse('detail_categ', args=[self.categ.idCat]) #idCat existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_categorie_detail_response_code_KO(self):
        url = reverse('detail_categ', args=[9999]) # idCat non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_categorie_create_response_code_OK(self):
        response = self.client.get(reverse('creer_categorie'))
        self.assertEqual(response.status_code, 200)
    
    def test_categorie_update_response_code_OK(self):
        url = reverse('change_categorie', args=[self.categ.idCat]) # idCat existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_categorie_update_response_code_KO(self):
        url = reverse('change_categorie', args=[9999]) # idCat non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_categorie_delete_response_code_OK(self):
        url = reverse('delete_categorie', args=[self.categ.idCat]) # idCat existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_categorie_delete_response_code_KO(self):
        url = reverse('delete_categorie', args=[9999]) # idCat non existant
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # Test redirection
    def test_redirect_after_categorie_creation(self):
        response = self.client.post(reverse('creer_categorie'), {'nomCat': 'CategoriePourTestRedirectionCreation'} )
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, '/monApp/categorie/2/')

    def test_redirect_after_categorie_updating(self):
        response = self.client.post(reverse('change_categorie', args=[self.categ.idCat]),
        data={"nomCat": "CategoriePourTestRedirectionMaj"})
        # Statut 302 = redirection
        self.assertEqual(response.status_code, 302)
        # Redirection vers la vue de detail
        self.assertRedirects(response, f'/monApp/categorie/{self.categ.idCat}/')

    def test_redirect_after_categorie_deletion(self):
        response = self.client.post(reverse('delete_categorie', args=[self.categ.pk]))
        # Vérifie qu'on a bien une redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('categories'))
        # Vérifie que la catégorie a bien été supprimée de la base
        self.assertFalse(Categorie.objects.filter(pk=self.categ.pk).exists())