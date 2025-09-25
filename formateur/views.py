from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from formateur.models import Formateur

# Create your views here.


@login_required
def liste_formateurs(request):
    formateurs = Formateur.objects.select_related('user').filter(statut=True)
    context = {
        'formateurs': formateurs
    }
    return render(request, 'formateur/liste.html', context)


@login_required
def detail_formateur(request, formateur_id):
    formateur = get_object_or_404(Formateur, id=formateur_id)
    cours = formateur.cours.all()
    sessions = formateur.sessions_formateur.all()

    context = {
        'formateur': formateur,
        'cours': cours,
        'sessions': sessions,
    }
    return render(request, 'formateur/detail.html', context)
