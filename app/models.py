from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, telephone, password=None, **extra_fields):
        if not telephone:
            raise ValueError("L'utilisateur doit avoir un numéro de téléphone")
        user = self.model(telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telephone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telephone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    telephone = models.CharField(max_length=15, unique=True)
    solde =models.CharField(max_length=10, unique=True, blank=True, null=True)
    revenu=models.CharField(max_length=10, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.telephone
    def has_module_perms(self, app_label):
       return self.is_superuser or self.groups.filter(permissions__codename='can_view_' + app_label).exists()

    def has_perm(self, perm, obj=None):
       return self.is_superuser or self.groups.filter(permissions__codename=perm).exists()

class UserProfile(models.Model):
    telephone= models.EmailField(unique=True,max_length=15)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.telephone} {self.motdepasse}"


class Category(models.Model):
    name = models.CharField(max_length=100)

class Vip(models.Model):
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Assurez-vous que cette catégorie existe
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    revenu_journalier = models.DecimalField(max_digits=10, decimal_places=2)
    revenu_annuel = models.DecimalField(max_digits=10, decimal_places=2)
    duree_de_vie = models.IntegerField()


class withdrawAccount(models.Model):
    nom_complet = models.CharField(max_length=100)
    compte = models.CharField(max_length=20)
    reseau = models.CharField(
        max_length=8,
        choices=[
            ('momo', 'MTN-MOMO'),
            ('moov', 'MOOV'),
            ('orange', 'Orange'),
        ],
        verbose_name="reseau",
        default='momo',
    )