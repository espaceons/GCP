from django.urls import path
from apprentis import views

app_name = "apprentis"

urlpatterns = [
    # CRUD Apprentis
    path("", views.liste_apprentis, name="liste_apprentis"),
    path("<int:apprenti_id>/", views.detail_apprenti, name="detail_apprenti"),
    path("ajouter/", views.ajouter_apprenti, name="ajouter_apprenti"),
    path("<int:apprenti_id>/modifier/",
         views.modifier_apprenti, name="modifier_apprenti"),
    path("<int:apprenti_id>/supprimer/",
         views.supprimer_apprenti, name="supprimer_apprenti"),

    # Inscriptions
    path("inscriptions/", views.liste_inscriptions, name="liste_inscriptions"),

    # ✅ Route pour l’inscription à un pack depuis la liste des apprentis.
    path('<int:apprenti_id>/inscrire/',
         views.inscrire_pack, name='inscrire_pack'),



    path("inscriptions/ajouter/", views.ajouter_inscription,
         name="ajouter_inscription"),
    path("inscriptions/<int:inscription_id>/",
         views.detail_inscription, name="detail_inscription"),
    path("inscriptions/<int:inscription_id>/modifier/",
         views.modifier_inscription, name="modifier_inscription"),
    path("inscriptions/<int:inscription_id>/supprimer/",
         views.supprimer_inscription, name="supprimer_inscription"),
]
