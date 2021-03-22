from django.utils.translation import gettext as _
from initiatives.models import (
    BothersInitiativeArea, BothersInitiativeAppraiser, BothersInitiativeContractor,
    IdeaInitiativeArea, IdeaInitiativeAppraiser, IdeaInitiativeContractor,
    InterestedInitiativeArea, InterestedInitiativeAppraiser, Initiative, StatusInitiative,
    User, Reviwers
)
from initiatives.utils import send_email

from datetime import datetime, timedelta
from django.utils import timezone
from collections import defaultdict
from behaviors.behaviors import Published

import logging
logger = logging.getLogger(__name__)


def send_daily_notifications():
    models = [
        BothersInitiativeArea, BothersInitiativeAppraiser, BothersInitiativeContractor,
        IdeaInitiativeArea, IdeaInitiativeAppraiser, IdeaInitiativeContractor,
        InterestedInitiativeArea, InterestedInitiativeAppraiser
    ]
    subject = _('New initiatives which needs you attention')
    email_initiatives = defaultdict(list)
    for model in models:
        initiatives = model.objects.filter(modified__gte=timezone.now()-timedelta(days=1))
        print(f'There is {initiatives.count()} initiatives for update.')
        for initiative in initiatives:
            emails = []
            if initiative.reviewer_user:
                emails = [initiative.reviewer_user.emai]
            else:
                emails = list(User.objects.filter(
                    role=initiative.reviewer,
                    area=initiative.area
                ).values_list('email', flat=True))
            for email in emails:
                email_initiatives[email].append(initiative)

    for email, initiatives in email_initiatives.items():
        send_email(
            subject,
            email,
            'emails/daily_notification_email.html',
            {
                'initiatives': initiatives
            }
        )
    print(email_initiatives)

def send_admin_daily_notifications():
    new_initiatives = Initiative.objects.filter(created__gte=timezone.now()-timedelta(days=1))
    status_inititives = StatusInitiative.objects.filter(
        created__gte=timezone.now()-timedelta(days=1),
        publication_status=Published.DRAFT
    )
    old_status_inititives = StatusInitiative.objects.filter(
        publication_status=Published.DRAFT
    ).exclude(id__in=status_inititives.values_list('id', flat=True))

    emails = [admin.email for admin in User.objects.filter(role=Reviwers.SUPER_ADMIN)]
    subject = _('New initiatives which needs you attention')

    initiatives = [status_inititive for status_inititive in status_inititives]
    old_initiatives = [status_inititive for status_inititive in old_status_inititives]
    for email in emails:
        send_email(
                subject,
                email,
                'emails/daily_admin_notification_email.html',
                {
                    'initiatives': initiatives,
                    'old_initiatives': old_initiatives
                }
            )
    print(emails, initiatives, old_initiatives)



