from __future__ import absolute_import, unicode_literals

from django.utils.translation import gettext as _
from django.conf import settings
from django.utils import timezone

from initiatives.models import (
    BothersInitiativeArea, BothersInitiativeAppraiser, BothersInitiativeContractor,
    IdeaInitiativeArea, IdeaInitiativeAppraiser, IdeaInitiativeContractor,
    InterestedInitiativeArea, InterestedInitiativeAppraiser, Initiative, StatusInitiative,
    User, Reviwers, Notification, Comment
)
from initiatives.utils import send_email

from datetime import datetime, timedelta
from collections import defaultdict
from behaviors.behaviors import Published

from celery import shared_task

from initiatives.utils import send_email


@shared_task
def send_email_task(subject, email, template, data, from_email=settings.FROM_EMAIL):
    send_email(
            subject,
            email,
            template,
            data,
            from_email
        )

@shared_task
def test_task():
    print('test')

@shared_task
def send_daily_notifications():
    subject = _('New initiatives which needs you attention')

    email_initiatives = defaultdict(list)

    notifications = Notification.objects.filter(is_sent=False).prefetch_related('initiative', 'for_user')

    for_superadmin = notifications.filter(
        for_user__role=Reviwers.SUPER_ADMIN
    ).distinct('initiative')
    for_non_superadmin = notifications.exclude(
        initiative__initiative_statuses__publication_status=Published.DRAFT
    )

    comments = Comment.objects.filter(
        created__gte=datetime.now()-timedelta(days=1)
    ).prefetch_related('initiative').order_by('created')

    super_admins = User.objects.filter(role=Reviwers.SUPER_ADMIN)

    for super_admin in super_admins:
        send_email(
            'New comments',
            super_admin.email,
            'emails/daily_notification_comments.html',
            {
                'comments': comments,
                'base_url': settings.BASE_URL
            }
        )


    for notification in for_superadmin:
        initiative = notification.initiative
        email_initiatives[notification.for_user.email].append({
            'initiative': initiative,
            'role': Reviwers.SUPER_ADMIN,
            'url': initiative.get_admin_url(Reviwers.SUPER_ADMIN),
        })

    for notification in for_non_superadmin:
        initiative = notification.initiative
        if notification.for_user:
            email_initiatives[notification.for_user.email].append({
                'initiative': initiative,
                'role': Reviwers.AREA_ADMIN,
                'url': initiative.get_admin_url(Reviwers.AREA_ADMIN),
            })
        else:
            area = notification.for_area
            area_admins = User.objects.filter(
                area=area,
                role=Reviwers.AREA_ADMIN)
            print(area_admins)
            for user in area_admins:
                email_initiatives[user.email].append({
                    'initiative': initiative,
                    'role': user.role,
                    'url': initiative.get_admin_url(user.role),
                })
    

    for email, initiatives in email_initiatives.items():
        send_email(
            subject,
            email,
            'emails/daily_notification_email.html',
            {
                'initiatives': initiatives,
                'base_url': settings.BASE_URL
            }
        )

    for_superadmin.update(is_sent=True)
    for_non_superadmin.update(is_sent=True)
