from django.shortcuts import render,redirect
import requests
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Vip
from .forms import CustomUserLoginForm
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomPasswordChangeForm
import json
from datetime import timedelta
from django.utils.timezone import now
from app.tasks import ajouter_revenu_journalier

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès")
            return redirect('login') 
        else:
            print(form.errors)  # Ajoutez cette ligne pour imprimer les erreurs dans la console
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserCreationForm()
    
    return render(request,'home.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']
            user = authenticate(request, telephone=telephone, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Vous êtes connecté avec succès.")
                return redirect('vip')  # Rediriger vers une page après connexion
            else:
                messages.error(request, "Numéro de téléphone ou mot de passe invalide.")
    else:
        form = CustomUserLoginForm()

    return render(request, 'login.html', {'form': form})

def vip(request):
    vip_items = Vip.objects.all() 
    
    return render(request,'vip.html',{'vip_items': vip_items})

def setting(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Évite la déconnexion
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('home')  # Redirige vers la page souhaitée après le changement de mot de passe
        else:
            
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request,'setting.html', {'form': form})


def historique(request):
    return render(request,'historique.html')

def historique_deposit(request):
    return render(request,'historique_deposit.html')

def historique_withdraw(request):
    return render(request,'historique_withdraw.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Évite la déconnexion
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('profile')  # Redirige vers la page souhaitée après le changement de mot de passe
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def deposit(request):
    return render(request,'deposit.html')



def dashboard(request):
    user=request.user
    return render(request, 'dashboard.html',{'user':user})

def me(request):
    user=request.user
    return render(request, 'me.html',{'user':user})

def vip_detail(request, vip_id):
    # Récupérer l'objet VIP avec l'ID passé dans l'URL
    vip = get_object_or_404(Vip, id=vip_id)
    return render(request, 'vip_detail.html', {'vip': vip})

def payer(request,vip_id):
    
    vip = get_object_or_404(Vip, id=vip_id)
    user = request.user  # Utilisateur actuel
    user_solde = Decimal(request.user.solde) if isinstance(request.user.solde, str) else request.user.solde

    if user_solde < vip.montant:
        messages.error(request, "Votre solde est insuffisant.")
        return render(request, 'vip_detail.html', {'vip': vip})
        
    else:   
    # Si le paiement est validé
     user.solde = user_solde - vip.montant  # Utiliser Decimal pour l'opération
    
     user.save()
     messages.success(request, "Paiement réussi.")
    
     

    ajouter_revenu_journalier.apply_async((user.id, vip.revenu_journalier), eta=now() + timedelta(days=1))
    