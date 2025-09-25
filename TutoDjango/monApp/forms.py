from django import forms
from .models import Produit, Categorie, Rayon, Status

class ContactUsForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    message = forms.CharField(max_length=1000)

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        #fields = '__all__'
        exclude = ('categorie', 'status')

class CategForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = '__all__'

class RayonForm(forms.ModelForm):
    class Meta:
        model = Rayon
        fields = '__all__'

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'
