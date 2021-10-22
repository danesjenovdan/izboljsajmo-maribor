from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.gis.geos import GEOSGeometry
from django.utils.html import mark_safe

from behaviors.models import Published

from initiatives.models import (
    Initiative, Zone,
    # users
    SuperAdminUser, AreaAdminUser, AreaAppraiserUser, ContractorAppraiserUser, User, RestorePassword, ConfirmEmail,
    StatusInitiativeHear, StatusInitiativeEditing, StatusInitiativeProgress, StatusInitiativeFinished, StatusInitiativeDone,
    StatusInitiativeRejected, InitiativeType, BasicUser, Notification, Reviwers, NotificationType, BothersInitiativeSuper,
    BothersInitiativeArea, IdeaInitiativeSuper, IdeaInitiativeArea, InterestedInitiativeSuper, InterestedInitiativeArea,
)
from initiatives.utils import send_email, id_generator
from initiatives.tasks import send_email_task

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


def check_if_area_is_changed(sender, instance, **kwargs):
    old_instance = sender.objects.filter(id=instance.id)
    if old_instance:
        old_instance = old_instance[0]
    else:
        return
    logger.warning(f'{old_instance.area} {instance.area}')
    if old_instance.area != instance.area:
        logger.warning(f'area was changed')
        Notification(
            for_area=instance.area,
            initiative=instance,
            type=NotificationType.UPDATED
        ).save()
        Notification.objects.filter(
            for_area=old_instance.area,
            initiative=instance
        ).delete()


# initiatives signals
def set_zone_from_location(sender, instance, **kwargs):
    old_instance = sender.objects.filter(id=instance.id)
    if old_instance:
        old_location = old_instance[0].location
    else:
        old_location = None

    # set zone from location
    if instance.id is None and instance.location:
        zones = Zone.objects.filter(polygon__intersects=instance.location)
        if zones:
            instance.zone = zones[0]
    elif old_location == None and instance.location != None:
        zones = Zone.objects.filter(polygon__intersects=instance.location)
        if zones:
            instance.zone = zones[0]

    elif instance.location and instance.location.distance(old_location)*100 > 1:
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
            subject = _('Ponastavitev gesla za dostop do platforme Izboljšajmo Maribor')
            template = 'emails/restore_password.html'
            url = f'{settings.FRONT_URL}pozabljeno-geslo/{instance.key}/'
        elif sender == ConfirmEmail:
            subject = _('Potrditev registracije na platformi Izboljšajmo Maribor')
            template = 'emails/confirm_email.html'
            url = f'{settings.FRONT_URL}potrdi-racun/{instance.key}/'

        send_email_task.delay(
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
        # send email to initiator
        initiative = instance.initiative
        send_email_task.delay(
            f'#{initiative.id} {initiative.title}',
            initiative.author.email,
            'emails/response_for_user.html',
            {
                'content': mark_safe(instance.email_content.replace('\n', '</br>'))
            }
        )
        instance.is_email_sent = True
        instance.save()
        # create notification for admins
        if initiative.reviewer == Reviwers.AREA_ADMIN:
            Notification(
                for_area=initiative.area,
                initiative=initiative,
                type=NotificationType.UPDATED
            ).save()
        elif initiative.reviewer in [Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER]:
            Notification(
                for_user=initiative.reviewer_user,
                initiative=initiative,
                type=NotificationType.UPDATED
            ).save()



def notify_superadmin_for_new_status_initiative(sender, instance, created, **kwargs):
    if created and instance.publication_status == Published.DRAFT:
        users = User.objects.filter(role=Reviwers.SUPER_ADMIN)
        for user in users:
            Notification(
                initiative=instance.initiative,
                type=NotificationType.UPDATED,
                for_user=user
            ).save()


# TODO move this ti view od serializer
def send_email_after_initiative_created(sender, instance, created, **kwargs):
    if created:
        if instance.type == InitiativeType.BOTHERS_ME:
            template = 'emails/bothers.html'
        elif instance.type == InitiativeType.HAVE_IDEA:
            template = 'emails/idea.html'
        elif instance.type == InitiativeType.INTERESTED_IN:
            template = 'emails/interested.html'
        send_email_task.delay(
            f'#{instance.id} {instance.title}',
            instance.author.email,
            template,
            {}
        )

def check_is_blocked(sender, instance, created, **kwargs):
    if instance.blocked and not instance.blocked_email_sent:
        send_email_task.delay(
            f'Blokada elektronskega naslova',
            instance.email,
            'emails/blocked.html',
            {'user': instance}
        )
        instance.blocked_email_sent = True
        instance.is_active = False
        instance.save()

    logger.warning(f'{instance.note}{instance._old_note}')
    if instance.note != instance._old_note:
        logger.warning(f'SEND EMAIL')
        send_email_task.delay(
            f'{_("Opis uporabnika je bil spremenjen: ")} {instance.username}',
            settings.EMAIL_FOR_NEW_NOTIFICATIONS,
            'emails/user_note.html',
            {
                'username': instance.username,
                'note': instance.note
            }
        )

post_save.connect(set_contractor_appraiser_to_group, sender=ContractorAppraiserUser)
post_save.connect(set_area_appraiser_to_group, sender=AreaAppraiserUser)
post_save.connect(set_super_admin_to_group, sender=SuperAdminUser)
post_save.connect(set_area_admin_to_group, sender=AreaAdminUser)

pre_save.connect(set_zone_from_location, sender=Initiative)
#post_save.connect(send_email_after_initiative_created, sender=Initiative)

pre_save.connect(check_if_area_is_changed, sender=BothersInitiativeSuper)
pre_save.connect(check_if_area_is_changed, sender=BothersInitiativeArea)
pre_save.connect(check_if_area_is_changed, sender=IdeaInitiativeSuper)
pre_save.connect(check_if_area_is_changed, sender=IdeaInitiativeArea)
pre_save.connect(check_if_area_is_changed, sender=InterestedInitiativeSuper)
pre_save.connect(check_if_area_is_changed, sender=InterestedInitiativeArea)

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

post_save.connect(notify_superadmin_for_new_status_initiative, sender=StatusInitiativeHear)
post_save.connect(notify_superadmin_for_new_status_initiative, sender=StatusInitiativeEditing)
post_save.connect(notify_superadmin_for_new_status_initiative, sender=StatusInitiativeProgress)
post_save.connect(notify_superadmin_for_new_status_initiative, sender=StatusInitiativeFinished)
post_save.connect(notify_superadmin_for_new_status_initiative, sender=StatusInitiativeDone)
post_save.connect(notify_superadmin_for_new_status_initiative, sender=StatusInitiativeRejected)

