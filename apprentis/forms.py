from django import forms
from .models import Apprenti, Inscription


class ApprentiForm(forms.ModelForm):
    class Meta:
        model = Apprenti
        fields = ["nom", "prenom", "email",
                  "telephone", "date_naissance", "adresse"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control"}),
            "prenom": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "telephone": forms.TextInput(attrs={"class": "form-control"}),
            "adresse": forms.TextInput(attrs={"class": "form-control"}),
            "date_naissance": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ["apprenti", "pack", "statut"]
        widgets = {
            "apprenti": forms.Select(attrs={"class": "form-control"}),
            "pack": forms.Select(attrs={"class": "form-control"}),
            "statut": forms.Select(attrs={"class": "form-control"}),
        }
