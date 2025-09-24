from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from param.models import Cours, Session
# Create your views here.


@login_required
def sessionsliste(request):
    sessions = Session.objects.select_related('cours', 'formateur').all()
    context = {
        'sessions': sessions,
    }
    return render(request, 'param/sessionsliste.html', context)


@login_required
def detail_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    inscriptions = session.inscriptions.select_related('apprenti').all()
    context = {
        'session': session,
        'inscriptions': inscriptions,
    }
    return render(request, 'param/sessions_detail.html', context)


@login_required
def coursliste(request):
    cours = Cours.objects.select_related('formateur').filter(actif=True)
    context = {
        'cours': cours,
    }
    return render(request, 'param/coursliste.html', context)


@login_required
def detail_cours(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    sessions = cours.sessions.select_related('formateur').all()
    context = {
        'cours': cours,
        'sessions': sessions,
    }
    return render(request, 'param/cours_detail.html', context)
