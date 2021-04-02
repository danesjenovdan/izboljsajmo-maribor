from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.gis.geos import GEOSGeometry
from django.utils.html import mark_safe

from behaviors.behaviors import Published

from initiatives.models import (
    Initiative, Zone,
    # users
    SuperAdminUser, AreaAdminUser, AreaAppraiserUser, ContractorAppraiserUser, User, RestorePassword, ConfirmEmail,
    StatusInitiativeHear, StatusInitiativeEditing, StatusInitiativeProgress, StatusInitiativeFinished, StatusInitiativeDone,
    StatusInitiativeRejected, InitiativeType, BasicUser
)
from .utils import send_email, id_generator

import logging
logger = logging.getLogger(__name__)



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
            template = 'emails/confirm_email.html'
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


def send_status_initiative_response(sender, instance, created, **kwargs):
    if instance.publication_status == Published.PUBLISHED and not instance.is_email_sent:
        initiative = instance.initiative
        send_email(
            f'#{initiative.id} {initiative.title}',
            initiative.author.email,
            'emails/response_for_user.html',
            {
                'content': mark_safe(instance.email_content.replace('\n', '</br>'))
            }
        )
        instance.is_email_sent = True
        instance.save()

def send_email_after_initiative_created(sender, instance, created, **kwargs):
    if created:
        if instance.type == InitiativeType.BOTHERS_ME:
            template = 'emails/bothers.html'
        elif instance.type == InitiativeType.HAVE_IDEA:
            template = 'emails/idea.html'
        elif instance.type == InitiativeType.INTERESTED_IN:
            template = 'emails/interested.html'
        send_email(
            f'#{instance.id} {instance.title}',
            instance.author.email,
            template,
            {}
        )

def check_is_blocked(sender, instance, created, **kwargs):
    if instance.blocked and not instance.blocked_email_sent:
        send_email(
            f'Blokada elektronskega naslova',
            instance.email,
            'emails/blocked.html',
            {'user': instance}
        )
        instance.blocked_email_sent = True
        instance.is_active = False
        instance.save()

post_save.connect(set_contractor_appraiser_to_group, sender=ContractorAppraiserUser)
post_save.connect(set_area_appraiser_to_group, sender=AreaAppraiserUser)
post_save.connect(set_super_admin_to_group, sender=SuperAdminUser)
post_save.connect(set_area_admin_to_group, sender=AreaAdminUser)

pre_save.connect(set_zone_from_location, sender=Initiative)
post_save.connect(send_email_after_initiative_created, sender=Initiative)

post_save.connect(set_key, sender=RestorePassword)
post_save.connect(set_key, sender=ConfirmEmail)
post_save.connect(send_confirm_emil, sender=User)
post_save.connect(check_is_blocked, sender=BasicUser)

post_save.connect(send_status_initiative_response, sender=StatusInitiativeHear)
post_save.connect(send_status_initiative_response, sender=StatusInitiativeEditing)
post_save.connect(send_status_initiative_response, sender=StatusInitiativeProgress)
post_save.connect(send_status_initiative_response, sender=StatusInitiativeFinished)
post_save.connect(send_status_initiative_response, sender=StatusInitiativeDone)
post_save.connect(send_status_initiative_response, sender=StatusInitiativeRejected)

