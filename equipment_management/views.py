from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..equipment.models import CustomUser, Equipment, Maintenance, Notification
from ..equipment.serializers import UserSerializer, EquipmentSerializer, MaintenanceSerializer, NotificationSerializer

# ✅ ViewSet للمستخدمين
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # يتطلب تسجيل الدخول للوصول إلى البيانات

# ✅ ViewSet للمعدات
class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]

# ✅ ViewSet للصيانة
class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

# ✅ ViewSet للإشعارات
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
