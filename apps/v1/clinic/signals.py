import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Hospital, Service

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Hospital)
def log_hospital_update(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New hospital created: {instance.name}")
    else:
        logger.info(f"Hospital updated: {instance.name}")

@receiver(post_save, sender=Service)
def log_service_update(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New service created: {instance.title}")
    else:
        logger.info(f"Service updated: {instance.title}")