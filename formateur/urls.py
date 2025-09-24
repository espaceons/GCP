
from django.urls import path
from . import views


app_name = 'formateur'

urlpatterns = [
    # Formateurs
    path('formateurs/', views.liste_formateurs, name='liste_formateurs'),
    path('formateurs/<int:formateur_id>/',
         views.detail_formateur, name='detail_formateur'),
]
