from django import forms
from django.forms import inlineformset_factory
from .models import PackFormation, Programme


class PackFormationForm(forms.ModelForm):
    class Meta:
        model = PackFormation
        fields = ['titre', 'description', 'date_debut',
                  'date_fin', 'prix', 'nb_apprentis_max', 'actif']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'nb_apprentis_max': forms.NumberInput(attrs={'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        fields = ['titre', 'contenu', 'duree']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control'}),
            'duree': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Inline formset : permet d'ajouter plusieurs programmes dans un seul formulaire de Pack
ProgrammeFormSet = inlineformset_factory(
    PackFormation, Programme,
    form=ProgrammeForm,
    extra=1,  # nombre de formulaires vides par défaut
    can_delete=True
)
