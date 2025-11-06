from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import (
    Equipment, Maintenance, Notification,
    CustomUser, Panne
)

# ========== FORMULAIRES UTILISATEUR ==========

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirmez le mot de passe", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'must_change_password', 'role')


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'must_change_password')
    list_filter = ('is_staff', 'is_active', 'role', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informations personnelles'), {'fields': ('first_name', 'last_name')}),
        (_('Rôle & Sécurité'), {'fields': ('role', 'must_change_password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


# ========== ÉQUIPEMENT ==========

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'serial_number', 'purchase_date', 'purchase_cost', 'usage_hours', 'state')
    list_filter = ('type', 'state')
    search_fields = ('name', 'serial_number')


# ========== MAINTENANCE, NOTIFICATIONS ==========

admin.site.register(Maintenance)
admin.site.register(Notification)


# ========== PANNE ==========

@admin.register(Panne)
class PanneAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'description', 'date_signalement', 'est_resolue', 'date_resolution', 'signalee_par')
    list_filter = ('est_resolue', 'date_signalement')
    search_fields = ('equipment__name', 'description', 'signalee_par__email')
    date_hierarchy = 'date_signalement'


# ========== UTILISATEUR ==========

admin.site.register(CustomUser, CustomUserAdmin)
