from django.contrib import admin

from param.models import Cours, Session

# Register your models here.


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'formateur', 'niveau', 'prix', 'actif')
    list_filter = ('niveau', 'actif', 'formateur')
    search_fields = ('titre', 'description')


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('cours', 'formateur', 'date_debut',
                    'date_fin', 'statut', 'places_restantes')
    list_filter = ('statut', 'date_debut', 'cours')
    search_fields = ('cours__titre', 'salle')
