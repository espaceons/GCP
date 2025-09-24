from django.contrib import admin

from apprentis.models import Apprenti, Inscription

# Register your models here.


@admin.register(Apprenti)
class ApprentiAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_naissance', 'date_inscription', 'statut')
    list_filter = ('statut', 'date_inscription')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('apprenti', 'session', 'date_inscription', 'statut')
    list_filter = ('statut', 'date_inscription')
    search_fields = ('apprenti__user__username', 'session__cours__titre')
