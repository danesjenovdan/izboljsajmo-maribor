import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class InitiativesConfig(AppConfig):
    name = "initiatives"

    def ready(self):
        import initiatives.signals
        import initiatives.tasks
