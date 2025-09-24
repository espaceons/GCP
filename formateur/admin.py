# formations/admin.py
from django.contrib import admin
from .models import Formateur


@admin.register(Formateur)
class FormateurAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialite', 'experience', 'statut')
    list_filter = ('statut', 'specialite')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
