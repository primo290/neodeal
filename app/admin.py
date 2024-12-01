from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('telephone', 'password','solde')
    list_filter = ('telephone',)
    fieldsets = (
        (None, {'fields': ('telephone', 'password','solde')}),
        
        ('Permissions', {'fields': ('is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('telephone', 'password'),
        }),
    )
    search_fields = ('telephone', 'password')
    ordering = ('telephone',)
    filter_horizontal = ()

admin.site.register(CustomUser, CustomUserAdmin)


# Ensure this block is only present once in your codebase
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('telephone', 'password')
    search_fields = ('telephone', 'password')

admin.site.register(UserProfile, UserProfileAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



class VipAdmin(admin.ModelAdmin):
    list_display = ('nom', 'montant', 'revenu_journalier', 'revenu_annuel', 'duree_de_vie')
    search_fields = ('nom',)
    list_filter = ('duree_de_vie',)
    ordering = ('-revenu_annuel',)

admin.site.register(Vip, VipAdmin)


class withdrawAccountAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'compte', 'reseau')
    search_fields = ('reseau',)
    list_filter = ('compte',)
    ordering = ('nom_complet',)

admin.site.register(withdrawAccount, withdrawAccountAdmin)
