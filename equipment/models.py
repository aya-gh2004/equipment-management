from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.utils import timezone
import datetime
from django.db import models
# ✅ Manager personnalisé
# models.py
# equipment/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse e-mail est requise")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
ROLE_CHOICES = [
    ('admin', 'Administrateur'),
    ('user', 'Utilisateur'),
    ('technicien', 'Technicien'),
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('adresse e-mail'), unique=True)
    first_name = models.CharField(_('prénom'), max_length=30, blank=True)
    last_name = models.CharField(_('nom'), max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    must_change_password = models.BooleanField(default=True)  # ✅ حقل جديد
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    # models.py — ajouter ce champ facultatif si vraiment nécessaire
    plain_password = models.CharField(max_length=128, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # aucun champ supplémentaire requis pour createsuperuser

    objects = CustomUserManager()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.email
 
STATE_CHOICES = [
        ('En fonctionnement', 'En fonctionnement'),
        ('En Panne', 'En Panne'),
        ('En Maintenance', 'En Maintenance'),
    ]
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2)
    lifetime_years = models.IntegerField()
    usage_hours = models.IntegerField()
    state = models.CharField(
        max_length=20,
        choices=STATE_CHOICES,
        default='En fonctionnement'
    ) 
    location = models.CharField(max_length=100)
    equipment_code = models.CharField(max_length=100)
    installation_date = models.DateField()
    last_maintenance_date = models.DateField()
    photo = models.ImageField(upload_to='equipment_photos/', blank=True, null=True)

    def __str__(self):
      return self.name


# ✅ Statistiques des équipements
class EquipementStatistiques(models.Model):
    total = models.IntegerField(default=0)
    en_panne = models.IntegerField(default=0)
    en_maintenance = models.IntegerField(default=0)

    def __str__(self):
        return f"Total: {self.total}, En Panne: {self.en_panne}, En Maintenance: {self.en_maintenance}"
class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('alerte', 'Alerte'),
        ('panne', 'Panne'),
    ]
    message = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    recipient_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    recipient_group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)  # ← أضف هذا السطر
    def __str__(self):
        return f"{self.type.upper()} - {self.message[:30]}..."


# ✅ Modèle Technicien lié à un utilisateur
class Technician(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='technician')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.utils.timezone import now

User = get_user_model()

class Maintenance(models.Model):
    machine = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    technicien = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    type = models.CharField(max_length=50, choices=[('Préventive', 'Préventive'), ('Corrective', 'Corrective')])
    status = models.CharField(max_length=50, choices=[('planifiee', 'Planifiée'), ('en_cours', 'En cours'), ('terminee', 'Terminée')])
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    photo_piece = models.ImageField(upload_to='maintenance_photos/', null=True, blank=True)
    lieu_correction = models.CharField(max_length=255, null=True, blank=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    rapport = models.TextField(null=True, blank=True)
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        previous_status = None

        if not is_new:
            try:
                previous = Maintenance.objects.get(pk=self.pk)
                previous_status = previous.status
            except Maintenance.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # فقط تحديث حالة الآلة وربط الأعطال
        if self.status == 'planifiee':
            self.machine.state = 'En Panne'
        elif self.status == 'en_cours':
            self.machine.state = 'En Maintenance'
        elif self.status == 'terminee':
            self.machine.state = 'En fonctionnement'

            # إغلاق الأعطال
            from .models import Panne
            Panne.objects.filter(equipment=self.machine, est_resolue=False).update(
                est_resolue=True, date_resolution=self.date_fin
            )

        self.machine.save()
        
from django.db import models

class Demande(models.Model):
    STATUT_CHOICES = [
        ('ouverte', 'Ouverte'),
        ('fermee', 'Fermée'),
        ('en_attente', 'En attente'),
    ]
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ouverte')

    def __str__(self):
        return self.titre
from django.contrib.auth import get_user_model
from .models import Notification
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Panne(models.Model):
    NIVEAU_URGENCE_CHOICES = [
        ('faible', 'Faible'),
        ('moyen', 'Moyen'),
        ('élevé', 'Élevé'),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='pannes/', null=True, blank=True)
    date_signalement = models.DateField(auto_now_add=True)
    est_resolue = models.BooleanField(default=False)
    date_resolution = models.DateField(null=True, blank=True)
    signalee_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    niveau_urgence = models.CharField(max_length=10, choices=NIVEAU_URGENCE_CHOICES, default='moyen')

    def __str__(self):
        return f"{self.equipment.name} - {self.description[:30]}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if self.equipment:
            if self.est_resolue:
                if self.equipment.state != 'En fonctionnement':
                    raise ValueError("Impossible de marquer la panne comme résolue si l'équipement n'est pas en fonctionnement.")
            else:
                self.equipment.state = 'En Panne'
                self.equipment.save()

        super().save(*args, **kwargs)

        


from django.conf import settings
from django.db import models

class AdminProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil Admin de {self.user.get_full_name() or self.user.email}"
from django.db import models

class Activite(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.email} - {self.description} - {self.date.strftime('%d/%m/%Y %H:%M')}"
