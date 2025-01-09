import logging
from collections import defaultdict
from datetime import datetime, timedelta

from behaviors.models import Published
from django.utils import timezone
from django.utils.translation import gettext as _
from initiatives.models import (
    BothersInitiativeAppraiser,
    BothersInitiativeArea,
    BothersInitiativeContractor,
    IdeaInitiativeAppraiser,
    IdeaInitiativeArea,
    IdeaInitiativeContractor,
    Initiative,
    InterestedInitiativeAppraiser,
    InterestedInitiativeArea,
    Reviwers,
    StatusInitiative,
    User,
)
from initiatives.utils import send_email

logger = logging.getLogger(__name__)


def send_daily_notifications():
    models = [
        BothersInitiativeArea,
        BothersInitiativeAppraiser,
        BothersInitiativeContractor,
        IdeaInitiativeArea,
        IdeaInitiativeAppraiser,
        IdeaInitiativeContractor,
        InterestedInitiativeArea,
        InterestedInitiativeAppraiser,
    ]
    subject = _("New initiatives which needs you attention")
    email_initiatives = defaultdict(list)
    for model in models:
        initiatives = model.objects.filter(
            modified__gte=timezone.now() - timedelta(days=1), is_draft=False
        )
        print(f"There is {initiatives.count()} initiatives for update.")
        for initiative in initiatives:
            emails = []
            if initiative.reviewer_user:
                emails = [initiative.reviewer_user.emai]
            else:
                emails = list(
                    User.objects.filter(
                        role=initiative.reviewer, area=initiative.area
                    ).values_list("email", flat=True)
                )
            for email in emails:
                email_initiatives[email].append(initiative)

    for email, initiatives in email_initiatives.items():
        send_email(
            subject,
            email,
            "emails/daily_notification_email.html",
            {"initiatives": initiatives},
        )
    print(email_initiatives)


def send_admin_daily_notifications():
    new_initiatives = Initiative.objects.filter(
        created__gte=timezone.now() - timedelta(days=1), is_draft=False
    )
    status_inititives = StatusInitiative.objects.filter(
        created__gte=timezone.now() - timedelta(days=1),
        publication_status=Published.DRAFT,
    )
    old_status_inititives = StatusInitiative.objects.filter(
        publication_status=Published.DRAFT
    ).exclude(id__in=status_inititives.values_list("id", flat=True))

    emails = [admin.email for admin in User.objects.filter(role=Reviwers.SUPER_ADMIN)]
    subject = _("New initiatives which needs you attention")

    initiatives = [status_inititive for status_inititive in status_inititives]
    old_initiatives = [status_inititive for status_inititive in old_status_inititives]
    for email in emails:
        send_email(
            subject,
            email,
            "emails/daily_admin_notification_email.html",
            {"initiatives": initiatives, "old_initiatives": old_initiatives},
        )
    print(emails, initiatives, old_initiatives)
