from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

from behaviors.behaviors import Published

# from .models import (
#     BothersInitiativeArea, BothersInitiativeSuper, BothersInitiativeContractor, StatusInitiative,

#     # users
#     SuperAdminUser, AreaAdminUser, AreaAppraiserUser, ContractorAppraiserUser, User
# )
from .utils import send_email

import logging
logger = logging.getLogger(__name__)

# TODO
def handle_super_admin_save(sender, instance, **kwargs):
    pass

# TODO
def handle_area_admin_save(sender, instance, **kwargs):
    pass

# TODO
def handle_contractor_save(sender, instance, **kwargs):
    pass

# TODO
def handle_status_save(sender, instance, **kwargs):
    if instance.publication_status == Published.PUBLISHED and instance.is_email_sent == False:
        instance.is_email_sent = True
        instance.save()



# set users to permissions groups
def set_super_admin_to_group(sender, instance, created, **kwargs):
    if created:
        admin_group = Group.objects.filter(name='Super admin')
        if admin_group:
            admin_group = admin_group[0]
            admin_group.user_set.add(instance)


def set_area_admin_to_group(sender, instance, created, **kwargs):
    if created:
        admin_group = Group.objects.filter(name='Area admin')
        if admin_group:
            admin_group = admin_group[0]
            admin_group.user_set.add(instance)


def set_area_appraiser_to_group(sender, instance, created, **kwargs):
    if created:
        admin_group = Group.objects.filter(name='Appraiser')
        if admin_group:
            admin_group = admin_group[0]
            admin_group.user_set.add(instance)


def set_contractor_appraiser_to_group(sender, instance, created, **kwargs):
    logger.warning("save contractor")
    if created:
        logger.warning("set group")
        admin_group = Group.objects.filter(name='Contractor')
        if admin_group:
            admin_group = admin_group[0]
            admin_group.user_set.add(instance)

