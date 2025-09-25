from django.urls import path
from . import views


app_name = 'param'

urlpatterns = [
    # Sessions
    path('sessions/', views.sessionsliste, name='sessionsliste'),
    path('sessions/<int:session_id>/',
         views.detail_session, name='detail_session'),
    # path('sessions/<int:session_id>/inscription/',
    #      views.inscription_session, name='inscription_session'),


    # Cours
    path('cours/', views.coursliste, name='coursliste'),
    path('cours/<int:cours_id>/', views.detail_cours, name='detail_cours'),


    # Packs
    path("packs/", views.liste_packs, name="pack_list"),
    path("packs/add/", views.ajouter_pack, name="pack_add"),
    path("packs/<int:pk>/edit/", views.modifier_pack, name="pack_edit"),
    path("packs/<int:pk>/delete/", views.supprimer_pack, name="pack_delete"),
]
