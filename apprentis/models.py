from django.db import models
from django.contrib.auth import get_user_model

from param.models import Session

User = get_user_model()
# Create your models here.


class Apprenti(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='apprenti')
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    date_inscription = models.DateField(auto_now_add=True)
    statut = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Apprenti"
        verbose_name_plural = "Apprentis"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.date_inscription.year}"


class Inscription(models.Model):
    apprenti = models.ForeignKey(
        Apprenti, on_delete=models.CASCADE, related_name='inscriptions')
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='inscriptions')
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=[
        ('inscrit', 'Inscrit'),
        ('attente', 'En Attente'),
        ('annule', 'Annulé'),
    ], default='inscrit')

    class Meta:
        unique_together = ['apprenti', 'session']
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"

    def __str__(self):
        return f"{self.apprenti} - {self.session}"
