from django.db import models
from django.contrib.auth import get_user_model
from param.models import PackFormation

User = get_user_model()
# Create your models here.


class Apprenti(models.Model):
    nom = models.CharField(max_length=200, null=True)
    prenom = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, default="migrations@exemple.com")
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Inscription(models.Model):
    apprenti = models.ForeignKey(
        Apprenti, related_name="inscriptions", on_delete=models.CASCADE)
    pack = models.ForeignKey(PackFormation, related_name="inscriptions",
                             on_delete=models.SET_NULL, null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[("en_attente", "En attente"),
                 ("confirmee", "Confirmée"),
                 ("annulee", "Annulée")],
        default="en_attente"
    )

    class Meta:
        unique_together = ("apprenti", "pack")  # évite les doublons

    def __str__(self):
        return f"{self.apprenti} → {self.pack}"
