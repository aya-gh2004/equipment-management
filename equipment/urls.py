from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

# استيراد جميع الدوال والكلاسات من views مباشرة
from .views import (
    logout_view, dashboard, statistiques_page_view,
    maintenance_view,  mark_as_read,
    statistiques_api, manage_users,
    AjouterEquipementAPIView, UserListView,
    EquipmentViewSet, MaintenanceViewSet, NotificationViewSet,
    CustomLoginView, ForcePasswordChangeView,
    notif_unread_count , UserDeleteAPIView,
    equipment_list, add_equipment, delete_equipment,DashboardDataAPIView,
    equipment_detail, edit_equipment, add_maintenance , PanneViewSet,create_panne,
)
from django.views.generic import RedirectView

from .views import MarkAllNotificationsAsReadView

from .views import user_notifications ,UnreadNotificationCountAPIView ,NotificationListAPIView, pdf ,create_panne_api
from .views import maintenance_data_api ,notifications_view ,PanneCreateAPIView
from . import views
# DRF Router
router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'pannes', PanneViewSet)
urlpatterns = [
    # -------- AUTHENTICATION --------
    path('', CustomLoginView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('change-password/', ForcePasswordChangeView.as_view(), name='force_password_change'),
    path('logout/', logout_view, name='logout_view'),

    # -------- DASHBOARD & HTML PAGES --------
    path('dashboard/', dashboard, name='dashboard'),
    path('statistiques/', statistiques_page_view, name='statistiques_page'),
    path('maintenance/', maintenance_view, name='maintenance'),

    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/verify/', views.verify_code, name='verify_code'),
    path('password-reset/set-new-password/', views.set_new_password, name='set_new_password'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    # -------- Equipements (HTML) --------
    path('equipments/', equipment_list, name='equipment_list'),
    path('equipment/add/', add_equipment, name='add_equipment'),
    path('equipments/delete/<int:id>/', delete_equipment, name='equipment_delete'),
    path('equipments/detail/<int:id>/', equipment_detail, name='equipment_detail'),
    path('equipments/edit/<int:id>/', edit_equipment, name='edit_equipment'),

    path('equipment/sexport/pdf/', views.export_pdf, name='export_pdf'),
    path('maintenance/update/<int:pk>/', views.update_maintenance, name='update_maintenance'),
    path('maintenance/edit/<int:pk>/', views.edit_maintenance, name='edit_maintenance'),
    path('maintenance/edit/<int:pk>/', views.edit_maintenance, name='edit_maintenance'),
    
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('api/pannes/create/', views.PanneCreateAPIView.as_view(), name='create_panne'),
    path('export/pdf/', views.export_maintenances_pdf, name='export_maintenances_pdf'),
    path('export/excel/', views.export_maintenances_excel, name='export_maintenances_excel'),
    path('equipments/export_excel/', views.export_excel, name='export_excel'),
    # -------- Users (HTML) --------
    path('users/', manage_users, name='user_list'),
    path('users/export/pdf/', views.export_pdf, name='export_pdf'),
    path('users/export/xl/', views.export_xl, name='export_xl'),
    
    path('equipments/pdf/', pdf, name='pdf'),
    # -------- API ROUTER (DRF) --------
    path('api/', include(router.urls)),

    # API لعرض قائمة المستخدمين
    path('api/users/', UserListView.as_view(), name='api_user_list'),

    # حذف مستخدم
    path('api/users/<int:id>/', views.UserDeleteAPIView.as_view(), name='user_delete'),
    
    path('api/maintenance-data/', maintenance_data_api, name='maintenance_data_api'),
    # -------- Notifications (HTML) --------
    path('api/dashboard-data/', DashboardDataAPIView.as_view(), name='dashboard-data'),
    # -------- Notifications (API) --------
     path('notifications/', views.notification_page, name='notification_page'),
   path('notifications/add/', views.add_notification, name='add_notification'),
   
    path('api/notifications/', user_notifications, name='user_notifications'),
path('notifications/mark-as-read/', mark_as_read, name='mark_as_read'),
    
    path('api/pannes/', PanneCreateAPIView.as_view(), name='create_panne'),
    
    path('notif/unread_count/', UnreadNotificationCountAPIView.as_view(), name='unread_notif_count'),

    path('notif/unread_count/', notif_unread_count, name='notif_unread_count'),
    path('notifications/', notifications_view, name='notifications'),
    path('api/notifications/', views.notification_list_create, name='notification_list_create'),
    path('notifications/delete/<int:pk>/', views.notification_delete, name='notification_delete'),
    path('api/users/', views.get_users, name='get_users'),
    path('api/groups/', views.get_groups, name='get_groups'),
    path('maintenance/', maintenance_view, name='maintenance'),
    path('maintenance/add/', add_maintenance, name='add_maintenance'),
    path('maintenance/delete/<int:maintenance_id>/', views.delete_maintenance, name='delete_maintenance'),
    path('maintenance/edit/<int:maintenance_id>/', views.edit_maintenance, name='edit_maintenance'),
   
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/users/<int:id>/delete/', UserDeleteAPIView.as_view(), name='user_delete_api'),
    path('notifications/mark-as-read/', MarkAllNotificationsAsReadView.as_view(), name='mark_notifications_as_read'),
    path('create-panne/', views.create_panne, name='create_panne'),
    path('pannes/', views.pannes_view, name='pannes'),
   # path('create/', views.create_panne, name='create_panne'),  # مثال: صفحة إضافة عطل
    path('api/pannes/<int:id>/', views.get_panne, name='api_get_panne'),
    path('api/pannes/<int:id>/update/', views.update_panne, name='api_update_panne'),
    path('api/pannes/<int:id>/delete/', views.delete_panne, name='api_delete_panne'),
    
    path('api/pannes/create/', create_panne_api, name='create_panne'),
    path('api/pannes/create/', create_panne, name='create_panne'),
    path("api/notifications/", NotificationListAPIView.as_view(), name="notifications_api"),
    path('api/pannes/create/', views.create_panne_api, name='create_panne_api'),   
    path('api/pannes/<int:id>/delete/', views.delete_panne, name='delete_panne'),
    path('pannes/<int:id>/', views.detail_panne, name='detail_panne'),
    path('pannes/<int:id>/modifier/', views.modifier_panne, name='modifier_panne'),
    # API لعرض الإحصائيات
    path('api/statistiques/', statistiques_api, name='statistiques_api'),
    path('api/dashboard/statistiques/', statistiques_api, name='api_dashboard_statistiques'),

    # -------- Custom APIs --------
    path('api/equipment/add/', AjouterEquipementAPIView.as_view(), name='api_ajout_equipement'),
]

# -------- Fichiers médias (en mode développement) --------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
