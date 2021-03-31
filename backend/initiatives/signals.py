from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.gis.geos import GEOSGeometry

from behaviors.behaviors import Published

from initiatives.models import (
    Initiative, Zone,
    # users
    SuperAdminUser, AreaAdminUser, AreaAppraiserUser, ContractorAppraiserUser, User, RestorePassword, ConfirmEmail
)
from .utils import send_email, id_generator

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
            instance.groups.add(admin_group[0])
            admin_group = admin_group[0]
            instance.is_staff = True
            instance.email_confirmed = True
            instance.save()


def set_area_admin_to_group(sender, instance, created, **kwargs):
    if created:
        admin_group = Group.objects.filter(name='Area admin')
        if admin_group:
            instance.groups.add(admin_group[0])
            admin_group = admin_group[0]
            instance.is_staff = True
            instance.email_confirmed = True
            instance.save()


def set_area_appraiser_to_group(sender, instance, created, **kwargs):
    if created:
        admin_group = Group.objects.filter(name='Appraiser')
        if admin_group:
            instance.groups.add(admin_group[0])
            admin_group = admin_group[0]
            instance.is_staff = True
            instance.email_confirmed = True
            instance.save()


def set_contractor_appraiser_to_group(sender, instance, created, **kwargs):
    if created:
        admin_group = Group.objects.filter(name='Contractor')
        if admin_group:
            instance.groups.add(admin_group[0])
            admin_group = admin_group[0]
            instance.is_staff = True
            instance.email_confirmed = True
            instance.save()


# initiatives signals
def set_zone_from_location(sender, instance, **kwargs):
    if instance.id is None and instance.location:
        zones = Zone.objects.filter(polygon__intersects=instance.location)
        if zones:
            instance.zone = zones[0]

    elif instance.location and instance.location.distance(sender.objects.get(id=instance.id).location)*100 > 1:
        zones = Zone.objects.filter(polygon__intersects=instance.location)
        if zones:
            instance.zone = zones[0]

# key generator
def set_key(sender, instance, created, **kwargs):
    if created:
        key = id_generator(size=32)
        not_unique = True
        while not_unique:
            key_gen = id_generator(size=32)
            not_unique = sender.objects.filter(key=key_gen)
        instance.key = key_gen
        instance.save()

        if sender == RestorePassword:
            subject = _('Restore password Izboljšajmo Maribor')
            template = 'emails/restore_password.html'
            url = f'{settings.FRONT_URL}pozabljeno-geslo/{instance.key}/'
        elif sender == ConfirmEmail:
            subject = _('Confirm email Izboljšajmo Maribor')
            template = 'emails/restore_password.html'
            url = f'{settings.FRONT_URL}potrdi-racun/{instance.key}/'

        send_email(
            subject,
            instance.user.email,
            template,
            {
                'url': url
            }
        )

def send_confirm_emil(sender, instance, created, **kwargs):
    if created:
        ConfirmEmail(user=instance).save()


post_save.connect(set_contractor_appraiser_to_group, sender=ContractorAppraiserUser)
post_save.connect(set_area_appraiser_to_group, sender=AreaAppraiserUser)
post_save.connect(set_super_admin_to_group, sender=SuperAdminUser)
post_save.connect(set_area_admin_to_group, sender=AreaAdminUser)

pre_save.connect(set_zone_from_location, sender=Initiative)

post_save.connect(set_key, sender=RestorePassword)
post_save.connect(set_key, sender=ConfirmEmail)
post_save.connect(send_confirm_emil, sender=User)
