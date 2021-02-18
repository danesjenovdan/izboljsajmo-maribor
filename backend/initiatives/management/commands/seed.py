from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Polygon, GEOSGeometry

from oauth2_provider.models import Application

from datetime import datetime

from initiatives import models
from initiative.models import InitiativeType, Initiative
from about.models import About, AboutType


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

        initiative = Initiative(
            type=InitiativeType.HAVE_IDEA,
            title='Bi bi dovilili vhod v vodnak pred univerzo',
            author=user,
            zone=zone,
            area=area,
            address='Ulica heroja Staneta 1, 2000 Maribor',
            location=GEOSGeometry('POINT(5 23)'),
            is_draft=False
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
            competent_service=competent_service
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

        About(
            order=1,
            type=AboutType.TITLE,
            content='O izboljšajmo Maribor',
            description='To je naslov'
        ).save()
        About(
            order=2,
            type=AboutType.TEXT,
            content='Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?',
            description='To je content'
        ).save()
        About(
            order=3,
            type=AboutType.IMAGE,
            url='https://img.youtube.com/vi/FcktgZewUok/0.jpg',
            description='To je slika'
        ).save()
        About(
            order=4,
            type=AboutType.TITLE2,
            content='Kako uporabljati platformo?',
            description='To je naslov'
        ).save()
        About(
            order=5,
            type=AboutType.YOUTUBE_EMBED,
            url='https://www.youtube.com/watch?v=GRLbU2JbBHY',
            description='To je YT video'
        ).save()
