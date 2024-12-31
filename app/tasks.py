from celery import shared_task
from django.contrib.auth.models import User

@shared_task
def ajouter_revenu_journalier(user_id, montant):
    user = User.objects.get(id=user_id)
    user.solde += montant
    user.save()
