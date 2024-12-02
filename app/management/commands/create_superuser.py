from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Créer un superutilisateur depuis une commande personnalisée."

    def add_arguments(self, parser):
        # Ajouter les arguments nécessaires
        parser.add_argument('--telephone', type=str, help="Téléphone du superutilisateur", required=True)
        parser.add_argument('--password', type=str, help="Mot de passe du superutilisateur", required=True)

    def handle(self, *args, **options):
        User = get_user_model()  # Récupère le modèle utilisateur
        telephone = options['telephone']
        password = options['password']

        if User.objects.filter(telephone=telephone).exists():
            self.stdout.write(self.style.ERROR(f"Un utilisateur avec ce numéro {telephone} existe déjà."))
        else:
            User.objects.create_superuser(telephone=telephone, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superutilisateur avec le numéro {telephone} créé avec succès."))
