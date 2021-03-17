from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from behaviors.behaviors import Published

from .models import (
    BothersInitiativeArea, BothersInitiativeSuper, BothersInitiativeContractor, StatusInitiative,

    # users
    SuperAdminUser, AreaAdminUser, AreaAppraiserUser, ContractorAppraiserUser
)
from .utils import send_email

# TODO
@receiver(pre_save, sender=BothersInitiativeSuper)
def handle_super_admin_save(sender, instance, **kwargs):
    pass

# TODO
@receiver(pre_save, sender=BothersInitiativeArea)
def handle_area_admin_save(sender, instance, **kwargs):
    pass

# TODO
@receiver(pre_save, sender=BothersInitiativeContractor)
def handle_contractor_save(sender, instance, **kwargs):
    pass

# TODO
@receiver(post_save, sender=StatusInitiative)
def handle_contractor_save(sender, instance, **kwargs):
    if instance.publication_status == Published.PUBLISHED and instance.is_email_sent == False:
        instance.is_email_sent = True
        instance.save()



# set users to permissions groups
@receiver(post_save, sender=SuperAdminUser)
def set_area_admin_to_group(sender, instance, **kwargs):
    admin_group = Group.objects.filter(name='Super admin')
    if admin_group:
        admin_group.user_set.add(instance)


@receiver(post_save, sender=AreaAdminUser)
def set_area_admin_to_group(sender, instance, **kwargs):
    admin_group = Group.objects.filter(name='Area admin')
    if admin_group:
        admin_group.user_set.add(instance)


@receiver(post_save, sender=AreaAppraiserUser)
def set_area_admin_to_group(sender, instance, **kwargs):
    admin_group = Group.objects.filter(name='Appraiser')
    if admin_group:
        admin_group.user_set.add(instance)


@receiver(post_save, sender=ContractorAppraiserUser)
def set_area_admin_to_group(sender, instance, **kwargs):
    admin_group = Group.objects.filter(name='Contractor')
    if admin_group:
        admin_group.user_set.add(instance)
