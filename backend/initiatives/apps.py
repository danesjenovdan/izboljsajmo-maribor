from django.apps import AppConfig
import logging
logger = logging.getLogger(__name__)

class InitiativesConfig(AppConfig):
    name = 'initiatives'
    def ready(self):
        import initiatives.signals
        import initiatives.tasks
