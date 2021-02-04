from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Polygon, GEOSGeometry

from oauth2_provider.models import Application

from datetime import datetime

from initiatives import models


class Command(BaseCommand):
    help = 'Setup data for development'

    def handle(self, *args, **options):
        organization = models.Organization(
            name='DJND',
            number_of_members=23
        )
        organization.save()

        user = models.User(
            first_name='The guy',
            username='The guy',
            email='test@test.com',
            is_active=True,
        )
        user.save()
        user.set_password('123123123')
        user.save()
        user.organizations.add(organization)

        Application(
            client_id='kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7',
            client_secret='54pWmrpj1y9FiwkUDofjeP4B5tbLQ4wW6F2wqsMT3JuQN4ApIqcveKlzOC1laQIJp8JpVi99EheHCkumEJ0o81J9f2uHK3eXjUdxprzDnWlsTuZM6cgv1Eo35KSr7Mfg',
            user=user,
            client_type='confidential',
            authorization_grant_type= 'password',
            name='client'
        ).save()

        zone = models.Zone(
            name='Tezno',
            polygon=Polygon( ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0)) )
        )
        zone.save()

        competent_service = models.CompetentService(
            name='Zavod za kulturo maribor',
            description='Zavod za kulturo v totem mariboru bla bla'
        )
        competent_service.save()

        area = models.Area(
            name='GOSPODARSTVO/TURIZEM',
            note='dogodki, prireditve, praznična okrasitev mesta, turistične table',
            competent_service=competent_service
        )
        area.save()

        statuses = [
            {
                'name': 'Slišimo',
                'note': '',
                'default_email': 'Bla Bla Bla'
            },
            {
                'name': 'Zavrnjeno',
                'note': 'Pa nemorš mi delat tega',
                'default_email': 'Bla Bla Bla'
            },
            {
                'name': 'Urejamo',
                'note': 'Zrihtal bomo takoj ko bo možno',
                'default_email': 'Bla Bla Bla'
            },
            {
                'name': 'V izvajanju',
                'note': 'Zrihtal bomo takoj ko bo možno',
                'default_email': 'Bla Bla Bla'
            },
            {
                'name': 'Izvedeno',
                'note': 'Poglej kak smo carji',
                'default_email': 'Bla Bla Bla'
            },
            {
                'name': 'Zaključeno',
                'note': 'Poglej kak smo carji',
                'default_email': 'Bla Bla Bla'
            },
        ]
        for status in statuses:
            status_obj = models.Status(
                name=status['name'],
                note=status['note'],
                default_email=status['default_email']
            )
            status_obj.save()
            status['obj'] = status_obj

        initiative = models.Initiative(
            type=models.InitiativeType.HAVE_IDEA,
            title='Bi bi dovilili vhod v vodnak pred univerzo',
            author=user,
            zone=zone,
            area=area,
            location=GEOSGeometry('POINT(5 23)')
        )
        initiative.save()

        models.StatusInitiative(
            initiative=initiative,
            status=statuses[0]['obj'],
            note='Čuli smo tvoj predlog'
        ).save()

        models.StatusInitiative(
            initiative=initiative,
            status=statuses[2]['obj'],
            note='Pa nemorš mi tega delat'
        ).save()

        models.Comment(
            initiative=initiative,
            content='Super ideja <3',
            author=user,
            status=models.CommentStatus.PUBLISHED
        ).save()

        models.Vote(
            initiative=initiative,
            author=user,
        ).save()

        models.FAQ(
            question='Kolk cajta se popravla cesta',
            answer='Odvisno kolk je razrita'
        ).save()

        models.Rejection(
            name='Bedn predlog',
            note='Daj nea mi guši s takimi forami'
        ).save()

        models.Rejection(
            name='Bedn predlog',
            note='Daj nea mi guši s takimi forami'
        ).save()
