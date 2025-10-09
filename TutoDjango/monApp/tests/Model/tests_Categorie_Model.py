from django.test import TestCase
from monApp.models import Categorie

class CategorieModelTest(TestCase):
    def setUp(self):
        self.categ = Categorie.objects.create(nomCat="CategoriePourTest")

    def test_categorie_create(self):
        self.assertEqual(self.categ.nomCat, "CategoriePourTest")

    def test_string_repr(self):
        self.assertEqual(str(self.categ), "CategoriePourTest")

    def test_categorie_update(self):
        self.categ.nomCat = "CategoriePourTests"
        self.categ.save()

        update_categ = Categorie.objects.get(idCat=self.categ.idCat)
        self.assertEqual(update_categ.nomCat, "CategoriePourTests")

    def test_categorie_delete(self):
        self.categ.delete()
        self.assertEqual(Categorie.objects.count(), 0)
