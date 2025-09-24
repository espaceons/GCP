from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from apprentis.models import Apprenti, Inscription
from param.models import Session

# Create your views here.


@login_required
def liste_apprentis(request):
    apprentis = Apprenti.objects.select_related('user').filter(statut=True)
    return render(request, 'formations/apprentis/liste.html', {'apprentis': apprentis})


@login_required
def detail_apprenti(request, apprenti_id):
    apprenti = get_object_or_404(Apprenti, id=apprenti_id)
    inscriptions = apprenti.inscriptions.select_related('session__cours').all()
    return render(request, 'formations/apprentis/detail.html', {
        'apprenti': apprenti,
        'inscriptions': inscriptions
    })


@login_required
def inscription_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    # Vérifier si l'utilisateur est un apprenti
    if hasattr(request.user, 'apprenti'):
        apprenti = request.user.apprenti

        # Vérifier si déjà inscrit
        if Inscription.objects.filter(apprenti=apprenti, session=session).exists():
            message = "Vous êtes déjà inscrit à cette session."
        elif session.places_restantes > 0:
            Inscription.objects.create(apprenti=apprenti, session=session)
            session.places_restantes -= 1
            session.save()
            message = "Inscription réussie !"
        else:
            message = "Plus de places disponibles pour cette session."
    else:
        message = "Seuls les apprentis peuvent s'inscrire aux sessions."

    return render(request, 'formations/inscription.html', {
        'session': session,
        'message': message
    })
