from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from behaviors.behaviors import Published

from .models import (
    BothersInitiativeArea, BothersInitiativeSuper, BothersInitiativeContractor, StatusInitiative
)
from .utils import send_email


@receiver(pre_save, sender=BothersInitiativeSuper)
def handle_super_admin_save(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=BothersInitiativeArea)
def handle_area_admin_save(sender, instance, **kwargs):
    pass

@receiver(pre_save, sender=BothersInitiativeContractor)
def handle_contractor_save(sender, instance, **kwargs):
    pass


@receiver(post_save, sender=StatusInitiative)
def handle_contractor_save(sender, instance, **kwargs):
    if instance.publication_status == Published.PUBLISHED and instance.is_email_sent == False:
        instance.is_email_sent = True
        instance.save()
