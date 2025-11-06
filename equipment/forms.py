from django import forms
from .models import Maintenance, Equipment
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.utils import timezone
from .models import Technician
# Login Form
# forms.py
class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
class MaintenanceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MaintenanceForm, self).__init__(*args, **kwargs)

        # تخصيص الحقل technicien حسب الدور
        if user and user.role == 'technicien':
            self.fields.pop('technicien', None)
        else:
            self.fields['technicien'].queryset = CustomUser.objects.filter(role='technician')

        # ✅ تنسيق التاريخ المتوقع من الإدخال
        self.fields['date_debut'].input_formats = ['%d/%m/%Y']
        self.fields['date_fin'].input_formats = ['%d/%m/%Y']

    class Meta:
        model = Maintenance
        fields = '__all__'
        widgets = {
            'date_debut': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'JJ/MM/AAAA',
            }, format='%d/%m/%Y'),

            'date_fin': forms.DateInput(attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'JJ/MM/AAAA',
            }, format='%d/%m/%Y'),
            'machine': forms.Select(attrs={'class': 'form-select'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le coût'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'rapport': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lieu_correction': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_piece': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'technicien': forms.Select(attrs={'class': 'form-select'}),
        }

from django import forms
from .models import CustomUser

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser  # ✅ النموذج الصحيح
        fields = ['email', 'first_name', 'last_name', 'role', 'is_active', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
            user.plain_password = password  # إن كنت تستخدمه في جدول مثلاً
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].label = "Est actif ?"
        
        self.fields['password'].label = "mot de passe"
from django import forms
from .models import Panne

class PanneForm(forms.ModelForm):
    class Meta:
        model = Panne
        fields = ['equipment', 'description', 'image', 'niveau_urgence', 'est_resolue']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'niveau_urgence': forms.Select(),
            'est_resolue': forms.CheckboxInput(),
        }

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Votre adresse e-mail")
class VerificationCodeForm(forms.Form):
    code = forms.CharField(label="Code de vérification", max_length=6)
class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
from django import forms

class VerificationCodeForm(forms.Form):
    code = forms.CharField(label="Code de vérification", max_length=6)

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(label="Nouveau mot de passe", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmer le mot de passe", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        if password != confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data
