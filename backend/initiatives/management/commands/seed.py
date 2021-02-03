from initiatives import models

from django.core.management.base import BaseCommand, CommandError
from oauth2_provider.models import Application

from datetime import datetime


class Command(BaseCommand):
    help = 'Setup data for development'

    def handle(self, *args, **options):
        user = models.User(
            first_name='admin',
            username='admin',
            email='test@test.com',
            is_active=True
        )
        user.save()
        user.set_password('123123123')
        user.save()

        Application(
            client_id='kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7',
            client_secret='54pWmrpj1y9FiwkUDofjeP4B5tbLQ4wW6F2wqsMT3JuQN4ApIqcveKlzOC1laQIJp8JpVi99EheHCkumEJ0o81J9f2uHK3eXjUdxprzDnWlsTuZM6cgv1Eo35KSr7Mfg',
            user=user,
            client_type='confidential',
            authorization_grant_type= 'password',
            name='client'
        ).save()
