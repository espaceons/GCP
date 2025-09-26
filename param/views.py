from apprentis.models import Inscription
from .forms import PackFormationForm, PaiementForm, ProgrammeFormSet
from .models import PackFormation
from django.shortcuts import render, get_object_or_404, redirect
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


# CRUD Pack


@login_required
def liste_packs(request):
    packs = PackFormation.objects.all()
    return render(request, 'param/pack_liste.html', {'packs': packs})


@login_required
def detail_pack(request, pack_id):
    pack = get_object_or_404(PackFormation, id=pack_id)
    programmes = pack.programmes.all()
    return render(request, 'param/pack_detail.html', {'pack': pack, 'programmes': programmes})


@login_required
def ajouter_pack(request):
    if request.method == 'POST':
        form = PackFormationForm(request.POST)
        formset = ProgrammeFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            pack = form.save()
            formset.instance = pack
            formset.save()
            return redirect('param:pack_list')
    else:
        form = PackFormationForm()
        formset = ProgrammeFormSet()
    return render(request, 'param/pack_form.html', {'form': form, 'formset': formset, 'title': 'Ajouter un Pack'})


@login_required
def modifier_pack(request, pk):
    pack = get_object_or_404(PackFormation, id=pk)
    if request.method == 'POST':
        form = PackFormationForm(request.POST, instance=pack)
        formset = ProgrammeFormSet(request.POST, instance=pack)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('param:pack_list')
    else:
        form = PackFormationForm(instance=pack)
        formset = ProgrammeFormSet(instance=pack)
    return render(request, 'param/pack_form.html', {'form': form, 'formset': formset, 'title': 'Modifier le Pack'})


@login_required
def supprimer_pack(request, pk):
    pack = get_object_or_404(PackFormation, id=pk)
    if request.method == 'POST':
        pack.delete()
        return redirect('param:pack_list')
    return render(request, 'param/pack_confirm_delete.html', {'pack': pack})

# On ajouter un badge cliquable dans la liste des packs pour afficher les apprentis inscrits dans ce pack.


@login_required
def inscrits_pack(request, pack_id):
    pack = get_object_or_404(PackFormation, id=pack_id)
    inscriptions = Inscription.objects.filter(
        pack=pack).select_related("apprenti")
    return render(request, "param/inscrits_pack.html", {
        "pack": pack,
        "inscriptions": inscriptions,
    })


def ajouter_paiement(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)

    if request.method == "POST":
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.inscription = inscription
            paiement.save()
            return redirect("apprentis:detail_inscription", inscription.id)
    else:
        form = PaiementForm()

    return render(request, "apprentis/ajouter_paiement.html", {
        "form": form,
        "inscription": inscription
    })


# CRUD Programme de Formation
