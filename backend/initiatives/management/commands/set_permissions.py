from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _

from initiatives.models import (
    BothersInitiativeSuper, BothersInitiativeArea, BothersInitiativeContractor,
    IdeaInitiative, InterestedInitiative


class Command(BaseCommand):
    help = 'Setup data for development'

    def handle(self, *args, **options):


        content_type = ContentType.objects.get_for_model(BothersInitiativeArea, for_concrete_model=False)
        permission = Permission.objects.create(
            codename='can_publish',
            name=_('Area admin'),
            content_type=content_type,
        )
