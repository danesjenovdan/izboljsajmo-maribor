from django.utils.translation import gettext as _
from initiative.models import (
    BothersInitiativeArea, BothersInitiativeAppraiser, BothersInitiativeContractor,
    IdeaInitiativeArea, IdeaInitiativeAppraiser, IdeaInitiativeContractor,
    InterestedInitiativeArea, InterestedInitiativeAppraiser
)
from initiatives.utils import send_email

from datetime import datetime, timedelta
from collections import defaultdict


def send_daily_notifications():
    models = [
        BothersInitiativeArea, BothersInitiativeAppraiser, BothersInitiativeContractor,
        IdeaInitiativeArea, IdeaInitiativeAppraiser, IdeaInitiativeContractor,
        InterestedInitiativeArea, InterestedInitiativeAppraiser
    ]
    subject = _('New initiatives which needs you attention')
    email_initiatives = defaultdict(list)
    for model im models:
        initiatives = model.objects.filter(updated__gte=datetime.now()-timedelta(days=1))
        for initiative in initiatives:
            emails = []
            if initiative.reviewer_user:
                emails = [initiative.reviewer_user.emai]
            else:
                emails = list(User.objects.filter(
                    role=initiative.reviewer,
                    area=initiative.area
                ).values_list('email', flat=True))emails
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


