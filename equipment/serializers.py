from rest_framework import serializers
from .models import Equipment, Maintenance, Notification
from rest_framework import serializers



class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# serializers.py
from rest_framework import serializers
from .models import Panne

class PanneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panne
        fields = '__all__'
class PanneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panne
        fields = '__all__'
        read_only_fields = ['signalee_par', 'date_signalement']

from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
# users/serializers.py
# equipment/serializers.py
from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active', 'must_change_password']
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role', 'is_active', 'must_change_password']
from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']
# serializers.py

class PanneSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    signalee_par_email = serializers.EmailField(source='signalee_par.email', read_only=True)

    class Meta:
        model = Panne
        fields = '__all__'  # أو حدد الحقول بالتفصيل
