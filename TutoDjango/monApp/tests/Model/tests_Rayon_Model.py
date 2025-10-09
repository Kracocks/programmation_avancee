from django.test import TestCase
from monApp.models import Rayon

class RayonModelTest(TestCase):
    def setUp(self):
        self.rayon = Rayon.objects.create(nomRayon="RayonPourTest")

    def test_rayon_create(self):
        self.assertEqual(self.rayon.nomRayon, "RayonPourTest")

    def test_string_repr(self):
        self.assertEqual(str(self.rayon), "RayonPourTest")

    def test_rayon_update(self):
        self.rayon.nomRayon = "RayonPourTests"
        self.rayon.save()

        update_rayon = Rayon.objects.get(idRayon=self.rayon.idRayon)
        self.assertEqual(update_rayon.nomRayon, "RayonPourTests")

    def test_rayon_delete(self):
        self.rayon.delete()
        self.assertEqual(Rayon.objects.count(), 0)
