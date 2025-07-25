from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Notification
from django.contrib.auth.models import User


@receiver(post_save, sender=Order)
def notify_admin_on_payment(sender, instance, created, **kwargs):
    if instance.is_paid:
        # Créer une notif pour le superuser
        superusers = User.objects.filter(is_superuser=True) # type: ignore
        for admin in superusers:
            Notification.objects.create(
                user=admin,
                message=f"Nouvelle commande #{instance.id} de {instance.user.username}"
            )