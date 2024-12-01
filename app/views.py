from django.shortcuts import render,redirect
import requests
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Vip
from .forms import CustomUserLoginForm

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomPasswordChangeForm
import json

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


