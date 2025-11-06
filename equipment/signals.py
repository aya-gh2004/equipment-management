# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .models import Maintenance, Notification

User = get_user_model()

@receiver(post_save, sender=Maintenance)
def send_maintenance_notification(sender, instance, created, **kwargs):
    try:
        # فقط إذا status == terminee
        if instance.status == 'terminee':
            # تأكد أن الحالة تغيرت فعلاً
            if not created:
                old = Maintenance.objects.get(pk=instance.pk)
                if old.status == 'terminee':
                    return  # لا ترسل الإشعار مرتين

            # لكل مستخدم، أرسل إشعار لم يتم إرساله اليوم
            msg = f"L'équipement {instance.machine.name} a terminé sa maintenance et est retourné en fonctionnement."
            now_dt = now()
            for user in User.objects.all():
                deja = Notification.objects.filter(
                    recipient_user=user,
                    message=msg,
                    created_at__date=now_dt.date()
                ).exists()
                if not deja:
                    Notification.objects.create(
                        message=msg,
                        type='info',
                        recipient_user=user
                    )
    except Exception as e:
        print("Erreur dans le signal de maintenance:", e)
