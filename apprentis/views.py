from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apprentis.models import Apprenti, Inscription
from apprentis.forms import ApprentiForm, InscriptionForm
from param.forms import PaiementForm
from param.models import PackFormation, Paiement
from django.contrib import messages

# Liste / Ajouter / Modifier / supprime Apprenti

# liste des apprentis


@login_required
def liste_apprentis(request):
    apprentis = Apprenti.objects.all()
    context = {
        "apprentis": apprentis,
    }
    return render(request, "apprentis/liste_apprentis.html", context)

# ajouter Apprenti


@login_required
def ajouter_apprenti(request):
    if request.method == "POST":
        form = ApprentiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("apprentis:liste_apprentis")
    else:
        form = ApprentiForm()
    return render(request, "apprentis/ajouter_apprenti.html", {"form": form, "title": "Ajouter un Apprenti"})

# modifier Apprenti


@login_required
def modifier_apprenti(request, apprenti_id):
    apprenti = get_object_or_404(Apprenti, id=apprenti_id)

    # On récupère le paiement associé à l'inscription si existant
    # Première inscription si elle existe
    inscription = apprenti.inscriptions.first()
    paiement = Paiement.objects.filter(
        inscription=inscription).first() if inscription else None

    if request.method == "POST":
        apprenti_form = ApprentiForm(request.POST, instance=apprenti)
        paiement_form = PaiementForm(request.POST, instance=paiement)

        if apprenti_form.is_valid() and paiement_form.is_valid():
            apprenti_form.save()
            paiement_instance = paiement_form.save(commit=False)
            if inscription:
                paiement_instance.inscription = inscription
            paiement_instance.save()
            messages.success(
                request, "Apprenti et paiement mis à jour avec succès.")
            return redirect('apprentis:liste_apprentis')
    else:
        apprenti_form = ApprentiForm(instance=apprenti)
        paiement_form = PaiementForm(instance=paiement)

    return render(request, "apprentis/modifier_apprenti.html", {
        "apprenti_form": apprenti_form,
        "paiement_form": paiement_form,
        "apprenti": apprenti,
    })


# Supprimer Apprenti

@login_required
def supprimer_apprenti(request, apprenti_id):
    apprenti = get_object_or_404(Apprenti, id=apprenti_id)
    if request.method == "POST":
        apprenti.delete()
        return redirect("apprentis:liste_apprentis")
    return render(request, "apprentis/apprenti_confirm_delete.html", {"apprenti": apprenti})


# detail Apprenti

@login_required
def detail_apprenti(request, apprenti_id):
    # On récupère l'apprenti ou on renvoie une 404 si l'ID n'existe pas
    apprenti = get_object_or_404(Apprenti, id=apprenti_id)

    # Récupérer toutes les inscriptions liées à cet apprenti
    inscriptions = Inscription.objects.filter(apprenti=apprenti)

    return render(request, "apprentis/detail_apprenti.html", {
        "apprenti": apprenti,
        "inscriptions": inscriptions,
    })

# Liste / Ajouter / Modifier / Supprimer Inscription

# ajouter un apprentis a la platforme


@login_required
def ajouter_inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("param:liste_inscriptions")
    else:
        form = InscriptionForm()
    return render(request, "param/inscription_form.html", {"form": form, "title": "Inscrire un Apprenti"})


@login_required
def modifier_inscription(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)
    if request.method == "POST":
        form = InscriptionForm(request.POST, instance=inscription)
        if form.is_valid():
            form.save()
            return redirect("apprentis:liste_inscriptions")
    else:
        form = InscriptionForm(instance=inscription)
    return render(request, "apprentis/modifier_inscription.html", {"form": form})


# supprimer inscription

@login_required
def supprimer_inscription(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)
    if request.method == "POST":
        inscription.delete()
        return redirect("apprentis:liste_inscriptions")
    return render(request, "apprentis/supprimer_inscription.html", {"inscription": inscription})


# detail inscription

@login_required
def detail_inscription(request, inscription_id):
    inscription = get_object_or_404(Inscription, id=inscription_id)
    return render(request, "apprentis/detail_inscription.html", {"inscription": inscription})

# liste des inscriptions


@login_required
def liste_inscriptions(request):
    inscriptions = Inscription.objects.select_related("apprenti", "pack").all()

    return render(request, "apprentis/liste_inscriptions.html", {
        "inscriptions": inscriptions,
    })


# inscription a un pack

# @login_required
# def inscrire_pack(request, apprenti_id):
#     apprenti = get_object_or_404(Apprenti, id=apprenti_id)
#     packs = PackFormation.objects.filter(actif=True)
#     if request.method == 'POST':
#         pack_id = request.POST.get('pack')
#         pack = get_object_or_404(PackFormation, id=pack_id)
#         # Vérifie si l'inscription existe déjà
#         inscription, created = Inscription.objects.get_or_create(
#             apprenti=apprenti,
#             pack=pack,
#             defaults={'statut': 'en_attente'}
#         )
#         if not created:
#             messages.warning(
#                 request, "Cet apprenti est déjà inscrit à ce pack.")
#         else:
#             messages.success(request, "Inscription effectuée avec succès.")
#         return redirect('apprentis:liste_apprentis')
#     return render(request, 'apprentis/inscrire_pack.html', {'apprenti': apprenti, 'packs': packs})


@login_required
def inscrire_pack(request, apprenti_id):
    apprenti = get_object_or_404(Apprenti, id=apprenti_id)
    packs = PackFormation.objects.filter(actif=True)

    if request.method == "POST":
        pack_id = request.POST.get("pack")
        mode = request.POST.get("mode")  # récupère le mode choisi

        if not pack_id or not mode:
            messages.error(
                request, "Veuillez sélectionner un pack et un mode de paiement.")
            return redirect("apprentis:inscrire_pack", apprenti_id=apprenti.id)

        pack = get_object_or_404(PackFormation, id=pack_id)

        if Inscription.objects.filter(apprenti=apprenti, pack=pack).exists():
            messages.warning(
                request, "Cet apprenti est déjà inscrit dans ce pack.")
            return redirect("apprentis:liste_apprentis")

        # Création de l'inscription
        inscription = Inscription.objects.create(
            apprenti=apprenti,
            pack=pack,
            statut="en_attente"
        )

        # Création du paiement avec le mode choisi
        Paiement.objects.create(
            inscription=inscription,
            montant=pack.prix,
            mode=mode,
            statut="en_attente"
        )

        messages.success(
            request, f"{apprenti.prenom} {apprenti.nom} a été inscrit et le paiement a été généré.")
        return redirect("apprentis:liste_apprentis")

    return render(request, "apprentis/inscrire_pack.html", {"apprenti": apprenti, "packs": packs})
