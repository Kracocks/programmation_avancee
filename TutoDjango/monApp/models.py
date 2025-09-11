from django.db import models
from datetime import date

class Categorie(models.Model):
    idCat = models.AutoField(primary_key=True)
    nomCat = models.CharField(max_length=200)

    def __str__(self):
        return self.nomCat

class Status(models.Model):
    identifiant = models.AutoField(primary_key=True)
    libelle = models.CharField(max_length=200)

    def __str__(self):
        return self.libelle

class Produit(models.Model):
    refProd = models.AutoField(primary_key=True)
    intituleProd = models.CharField(max_length=200)
    prixUnitaireProd = models.DecimalField(max_digits=10, decimal_places=2)
    dateFabricationProd = models.DateField(null=False, default=date.today)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name="produits", null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="produits", null=True, blank=True)
    rayons = models.ManyToManyField("Rayon", through="Contenir", blank=True)

    def __str__(self):
        return self.intituleProd

class Rayon(models.Model):
    idRayon = models.AutoField(primary_key=True)
    nomRayon = models.CharField(max_length=200)
    produits = models.ManyToManyField("Produit", through="Contenir", blank=True)

    def __str__(self):
        return self.nomRayon

class Contenir(models.Model):
    produits = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name="produit")
    rayons = models.ForeignKey(Rayon, on_delete=models.CASCADE, related_name="rayons")
    quantite = models.IntegerField()

    class Meta:
        unique_together = ('produits', 'rayons')

    def __str__(self):
        return f"rayons {self.rayons} avec des {self.produits}"