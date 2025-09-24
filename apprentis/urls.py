
from django.urls import path
from . import views


app_name = 'apprentis'

urlpatterns = [
    # Apprentis
    path('', views.liste_apprentis, name='liste_apprentis'),
    path('<int:apprenti_id>/',
         views.detail_apprenti, name='detail_apprenti'),
]
