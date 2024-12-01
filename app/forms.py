from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,withdrawAccount
from .models import UserProfile  # Assurez-vous que UserProfile est bien importé s'il est utilisé dans la validation
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control w-full p-2 border border-gray-300 rounded-md', 'placeholder': 'Numéro de téléphone'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control w-full p-2 border border-gray-300 rounded-md', 'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control w-full p-2 border border-gray-300 rounded-md', 'placeholder': 'Confirmation'}))

    class Meta:
        model = CustomUser
        fields = ('telephone', 'password1', 'password2')
    
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if UserProfile.objects.filter(telephone=telephone).exists():
            raise forms.ValidationError("Ce numéro de téléphone existe déjà.")
        return telephone

class CustomUserLoginForm(forms.Form):
    telephone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'Numéro de téléphone'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'Mot de passe'
        })
    )






class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full pl-10 py-2 border border-gray-300 rounded-lg focus:border-orange-500 focus:ring-2 focus:ring-orange-200',
            'placeholder': 'Ancien mot de passe'
        })
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full pl-10 py-2 border border-gray-300 rounded-lg focus:border-orange-500 focus:ring-2 focus:ring-orange-200',
            'placeholder': 'Nouveau mot de passe'
        })
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full pl-10 py-2 border border-gray-300 rounded-lg focus:border-orange-500 focus:ring-2 focus:ring-orange-200',
            'placeholder': 'Confirmer le mot de passe'
        })
    )


