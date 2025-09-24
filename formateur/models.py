# formations/models.py
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Formateur(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='formateur')
    specialite = models.CharField(max_length=200)
    experience = models.IntegerField(default=0)  # années d'expérience
    telephone = models.CharField(max_length=20)
    date_embauche = models.DateField(auto_now_add=True)
    statut = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialite}"
