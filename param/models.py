from django.db import models
from django.utils import timezone
from formateur.models import Formateur

# Create your models here.


class Cours(models.Model):
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('avance', 'Avancé'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    formateur = models.ForeignKey(
        Formateur, on_delete=models.CASCADE, related_name='cours')
    duree = models.IntegerField(help_text="Durée en heures")  # Durée en heures
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

    def __str__(self):
        return f"{self.titre} - {self.formateur}"


class Session(models.Model):
    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]

    cours = models.ForeignKey(
        Cours, on_delete=models.CASCADE, related_name='sessions')
    formateur = models.ForeignKey(
        Formateur, on_delete=models.CASCADE, related_name='sessions_formateur')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    salle = models.CharField(max_length=100)
    places_max = models.IntegerField()
    places_restantes = models.IntegerField()
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='planifie')

    def __str__(self):
        return f"{self.cours.titre} - {self.date_debut.strftime('%d/%m/%Y')}"


# PAck de Formation / Programme de Formation :


class PackFormation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    nb_apprentis_max = models.PositiveIntegerField()
    actif = models.BooleanField(default=False)

    def __str__(self):
        return self.titre

    @property
    def nb_inscriptions(self):
        return self.inscriptions.count()


class Programme(models.Model):
    pack = models.ForeignKey(
        PackFormation, related_name="programmes", on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    duree = models.CharField(max_length=100, help_text="Ex: 2 jours, 10h")

    def __str__(self):
        return f"{self.titre} ({self.pack.titre})"


# paiement

class Paiement(models.Model):
    inscription = models.ForeignKey("apprentis.Inscription",
                                    related_name="paiements", on_delete=models.CASCADE
                                    )
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(default=timezone.now)
    mode = models.CharField(
        max_length=20,
        choices=[("especes", "Espèces"), ("cheque", "Chèque"),
                 ("virement", "Virement"), ("carte", "Carte bancaire")],
        default="especes"
    )
    statut = models.CharField(
        max_length=20,
        choices=[("en_attente", "En attente"),
                 ("valide", "Validé"), ("refuse", "Refusé")],
        default="en_attente"
    )

    def __str__(self):
        return f"{self.inscription.apprenti} → {self.montant} DT ({self.get_statut_display()})"
