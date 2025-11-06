from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # صفحة تسجيل الدخول
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),

    # تسجيل الخروج
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # تضمين جميع روابط تطبيق equipment (بما فيها: statistiques/api, dashboard, etc.)
    path('', include('equipment.urls')),

    # روابط auth الجاهزة مثل reset password وغيرها
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)