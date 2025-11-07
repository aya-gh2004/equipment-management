# equipment/forms_login.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


class EmailAuthenticationForm(AuthenticationForm):
    """
    نموذج مخصص لتسجيل الدخول عبر البريد الإلكتروني بدل اسم المستخدم.
    """
    username = forms.EmailField(
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre e-mail'})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Identifiants invalides. Veuillez réessayer.")
        return self.cleaned_data
