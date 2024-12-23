from datetime import datetime

from about import models as about_models
from about.models import About, AboutType
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis.geos import GEOSGeometry, Polygon
from django.core.management.base import BaseCommand, CommandError
from initiatives import models
from oauth2_provider.models import Application


class Command(BaseCommand):
    help = "Setup data for development"
    basc_options = [("change_", "Can change "), ("view_", "Can view ")]
    options = [("add_", "Can add "), ("change_", "Can change "), ("view_", "Can view ")]

    def handle(self, *args, **options):
        self.basc_options = [("change_", "Can change "), ("view_", "Can view ")]
        self.options = [
            ("add_", "Can add "),
            ("change_", "Can change "),
            ("view_", "Can view "),
        ]

        # Super admin
        admin_group, created = Group.objects.get_or_create(name="Super admin")

        ct = ContentType.objects.get_for_model(models.BothersInitiativeArea)
        permissions = self.get_permissions("bothersinitiativesuper", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.IdeaInitiativeAppraiser)
        permissions = self.get_permissions("ideainitiativesuper", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.InterestedInitiativeAppraiser)
        permissions = self.get_permissions(
            "interestedinitiativesuper", ct, self.options
        )
        admin_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.AreaAdminUser)
        permissions = self.get_permissions("areaadminuser", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.ContractorAppraiserUser)
        permissions = self.get_permissions("contractorappraiseruser", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.AreaAppraiserUser, self.options)
        permissions = self.get_permissions("areaappraiseruser", ct)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Image)
        permissions = self.get_permissions("image", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.File)
        permissions = self.get_permissions("file", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Area)
        permissions = self.get_permissions("area", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Zone)
        permissions = self.get_permissions("zone", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.User)
        permissions = self.get_permissions("user", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Comment)
        permissions = self.get_permissions(
            "comment", ct, [("view_", "Can view "), ("change_", "Can change ")]
        )
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Status)
        permissions = self.get_permissions("status", ct, self.basc_options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Rejection)
        permissions = self.get_permissions("rejection", ct, self.options)
        admin_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.StatusInitiativeHear)
        permissions = self.get_permissions("statusinitiativehear", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeEditing)
        permissions = self.get_permissions("statusinitiativeediting", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeProgress)
        permissions = self.get_permissions("statusinitiativeprogress", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeFinished)
        permissions = self.get_permissions("statusinitiativefinished", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeDone)
        permissions = self.get_permissions("statusinitiativedone", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeRejected)
        permissions = self.get_permissions("statusinitiativerejected", ct, self.options)
        admin_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(about_models.AboutTitle2)
        permissions = self.get_permissions("abouttitle2", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(about_models.AboutImage)
        permissions = self.get_permissions("aboutimage", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(about_models.AboutContent)
        permissions = self.get_permissions("aboutcontent", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(about_models.AboutYoutubeEmbed)
        permissions = self.get_permissions("aboutyoutubeembed", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(about_models.AboutTitle)
        permissions = self.get_permissions("abouttitle", ct, self.options)
        admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(about_models.About)
        permissions = self.get_permissions("about", ct, self.options)
        admin_group.permissions.add(*permissions)

        # Area admin
        area_admin_group, created = Group.objects.get_or_create(name="Area admin")

        ct = ContentType.objects.get_for_model(models.BothersInitiativeArea)
        permissions = self.get_permissions("bothersinitiativearea", ct)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.IdeaInitiativeAppraiser)
        permissions = self.get_permissions("ideainitiativearea", ct)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.InterestedInitiativeAppraiser)
        permissions = self.get_permissions("interestedinitiativearea", ct)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Image)
        permissions = self.get_permissions("image", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.File)
        permissions = self.get_permissions("file", ct, self.options)
        area_admin_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.User)
        permissions = self.get_permissions("user", ct, self.basc_options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.AreaAppraiserUser)
        permissions = self.get_permissions("areaappraiseruser", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.ContractorAppraiserUser)
        permissions = self.get_permissions("contractorappraiseruser", ct, self.options)
        area_admin_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.StatusInitiativeHear)
        permissions = self.get_permissions("statusinitiativehear", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeEditing)
        permissions = self.get_permissions("statusinitiativeediting", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeProgress)
        permissions = self.get_permissions("statusinitiativeprogress", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeFinished)
        permissions = self.get_permissions("statusinitiativefinished", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeDone)
        permissions = self.get_permissions("statusinitiativedone", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeRejected)
        permissions = self.get_permissions("statusinitiativerejected", ct, self.options)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Rejection)
        permissions = self.get_permissions("rejection", ct, self.read)
        area_admin_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Area)
        permissions = self.get_permissions("area", ct, self.read)
        area_admin_group.permissions.add(*permissions)

        # Appraiser group
        appraiser_group, created = Group.objects.get_or_create(name="Appraiser")
        ct = ContentType.objects.get_for_model(models.BothersInitiativeAppraiser)
        permissions = self.get_permissions("bothersinitiativeappraiser", ct)
        appraiser_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.IdeaInitiativeAppraiser)
        permissions = self.get_permissions("ideainitiativeappraiser", ct)
        appraiser_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.InterestedInitiativeAppraiser)
        permissions = self.get_permissions("interestedinitiativeappraiser", ct)
        appraiser_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.ContractorAppraiserUser)
        permissions = self.get_permissions("contractorappraiseruser", ct, self.options)
        appraiser_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.Image)
        permissions = self.get_permissions("image", ct, self.options)
        appraiser_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.File)
        permissions = self.get_permissions("file", ct, self.options)
        appraiser_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.StatusInitiativeEditing)
        permissions = self.get_permissions("statusinitiativeediting", ct, self.options)
        appraiser_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeProgress)
        permissions = self.get_permissions("statusinitiativeprogress", ct, self.options)
        appraiser_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeFinished)
        permissions = self.get_permissions("statusinitiativefinished", ct, self.options)
        appraiser_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeDone)
        permissions = self.get_permissions("statusinitiativedone", ct, self.options)
        appraiser_group.permissions.add(*permissions)

        # Contracotr group
        contractor_group, created = Group.objects.get_or_create(name="Contractor")
        ct = ContentType.objects.get_for_model(models.BothersInitiativeContractor)
        permissions = self.get_permissions("bothersinitiativecontractor", ct)
        contractor_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.IdeaInitiativeContractor)
        permissions = self.get_permissions("ideainitiativecontractor", ct)
        contractor_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.Image)
        permissions = self.get_permissions("image", ct, self.options)
        contractor_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.File)
        permissions = self.get_permissions("file", ct, self.options)
        contractor_group.permissions.add(*permissions)

        ct = ContentType.objects.get_for_model(models.StatusInitiativeEditing)
        permissions = self.get_permissions("statusinitiativeediting", ct, self.options)
        contractor_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeProgress)
        permissions = self.get_permissions("statusinitiativeprogress", ct, self.options)
        contractor_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeFinished)
        permissions = self.get_permissions("statusinitiativefinished", ct, self.options)
        contractor_group.permissions.add(*permissions)
        ct = ContentType.objects.get_for_model(models.StatusInitiativeDone)
        permissions = self.get_permissions("statusinitiativedone", ct, self.options)
        contractor_group.permissions.add(*permissions)

        organization = models.Organization(name="DJND", number_of_members=23)
        organization.save()

        user = models.User(
            first_name="The guy",
            username="The guy",
            email="test@test.com",
            is_active=True,
        )
        user.save()
        user.set_password("123123123")
        user.save()
        user.organizations.add(organization)

        Application(
            client_id="kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7",
            client_secret="54pWmrpj1y9FiwkUDofjeP4B5tbLQ4wW6F2wqsMT3JuQN4ApIqcveKlzOC1laQIJp8JpVi99EheHCkumEJ0o81J9f2uHK3eXjUdxprzDnWlsTuZM6cgv1Eo35KSr7Mfg",
            user=user,
            client_type="confidential",
            authorization_grant_type="password",
            name="client",
        ).save()

        zone = models.Zone(
            name="Tezno",
            polygon=Polygon(
                ((0.0, 0.0), (0.0, 50.0), (50.0, 50.0), (50.0, 0.0), (0.0, 0.0))
            ),
        )
        zone.save()

        competent_service = models.CompetentService(
            name="Zavod za kulturo maribor",
            description="Zavod za kulturo v totem mariboru bla bla",
        )
        competent_service.save()

        areas = [
            "KOMUNALNE STORITVE, PROMET, PROSTOR",
            "OKOLJE, NARAVA, ŽIVALI",
            "ŠPORT, REKREACIJA",
            "GOSPODARSTVO/TURIZEM",
            "KULTURA",
            "SOCIALNA VARNOST/ ZDRAVJE",
            "VZGOJA IN IZOBRAŽEVANJE, IZOBRAŽEVANJE ODRASLIH IN RAZVOJ KADROV ZA PODJETJA IN ORGANIZACIJE",
            "TRG DELA/ZAPOSLOVANJE",
            "DRUGO",
        ]
        for a in areas:
            area = models.Area(
                name=a, note="Napisi opis", competent_service=competent_service
            )
            area.save()

        gos_admin = models.User(
            first_name="gos admin",
            username="gos admin",
            email="admin@test.com",
            is_active=True,
        )
        gos_admin.save()
        gos_admin.set_password("123123123")
        gos_admin.save()
        gos_admin.competent_services.add(competent_service)

        admin_group.user_set.add(gos_admin)

        appraiser = models.User(
            first_name="gos appraiser",
            username="gos appraiser",
            email="appraiser@test.com",
            is_active=True,
        )
        appraiser.save()
        appraiser.set_password("123123123")
        appraiser.save()
        appraiser.competent_services.add(competent_service)

        appraiser_group.user_set.add(appraiser)

        statuses = [
            {"name": "Slišimo", "note": "", "default_email": "Bla Bla Bla"},
            {
                "name": "Zavrnjeno",
                "note": "Pa nemorš mi delat tega",
                "default_email": "Bla Bla Bla",
            },
            {
                "name": "Urejamo",
                "note": "Zrihtal bomo takoj ko bo možno",
                "default_email": "Bla Bla Bla",
            },
            {
                "name": "V izvajanju",
                "note": "Zrihtal bomo takoj ko bo možno",
                "default_email": "Bla Bla Bla",
            },
            {
                "name": "Izvedeno",
                "note": "Poglej kak smo carji",
                "default_email": "Bla Bla Bla",
            },
            {
                "name": "Zaključeno",
                "note": "Poglej kak smo carji",
                "default_email": "Bla Bla Bla",
            },
        ]
        for status in statuses:
            status_obj = models.Status(
                name=status["name"],
                note=status["note"],
                default_email=status["default_email"],
            )
            status_obj.save()
            status["obj"] = status_obj

        initiative = models.Initiative(
            type=models.InitiativeType.HAVE_IDEA,
            title="Bi bi dovilili vhod v vodnak pred univerzo",
            author=user,
            zone=zone,
            area=area,
            address="Ulica heroja Staneta 1, 2000 Maribor",
            location=GEOSGeometry("POINT(5 23)"),
            is_draft=False,
        )
        initiative.save()

        models.StatusInitiative(
            initiative=initiative,
            status=statuses[0]["obj"],
            note="Čuli smo tvoj predlog",
        ).save()

        models.StatusInitiative(
            initiative=initiative,
            status=statuses[2]["obj"],
            competent_service=competent_service,
        ).save()

        models.Comment(
            initiative=initiative,
            content="Super ideja <3",
            author=user,
            status=models.CommentStatus.PUBLISHED,
        ).save()

        models.Vote(
            initiative=initiative,
            author=user,
        ).save()

        models.FAQ(
            question="Kolk cajta se popravla cesta", answer="Odvisno kolk je razrita"
        ).save()

        models.Rejection(
            name="Bedn predlog", note="Daj nea mi guši s takimi forami"
        ).save()

        models.Rejection(
            name="Bedn avtor", note="Daj nea mi guši s takimi forami"
        ).save()

        About(
            order=1,
            type=AboutType.TITLE,
            content="O izboljšajmo Maribor",
            description="To je naslov",
        ).save()
        About(
            order=2,
            type=AboutType.TEXT,
            content="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?",
            description="To je content",
        ).save()
        About(
            order=3,
            type=AboutType.IMAGE,
            url="https://img.youtube.com/vi/FcktgZewUok/0.jpg",
            description="To je slika",
        ).save()
        About(
            order=4,
            type=AboutType.TITLE2,
            content="Kako uporabljati platformo?",
            description="To je naslov",
        ).save()
        About(
            order=5,
            type=AboutType.YOUTUBE_EMBED,
            url="https://www.youtube.com/watch?v=GRLbU2JbBHY",
            description="To je YT video",
        ).save()

        models.DescriptionDefinition(
            order=1,
            type=models.InitiativeType.HAVE_IDEA,
            title="Naslov opisa 1",
            field="title1",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=2,
            type=models.InitiativeType.HAVE_IDEA,
            title="Naslov opisa 2",
            field="title2",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=3,
            type=models.InitiativeType.HAVE_IDEA,
            title="Naslov opisa 3",
            field="title3",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=1,
            type=models.InitiativeType.BOTHERS_ME,
            title="Naslov opisa 1",
            field="title1",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=1,
            type=models.InitiativeType.INTERESTED_IN,
            title="Naslov opisa 1",
            field="title1",
            author_id=1,
        ).save()

    def get_permissions(self, name, ct, options=basc_options):
        permissions = []
        for option in options:
            print(f"{option[0]}{name}")
            permissions.append(Permission.objects.get(codename=f"{option[0]}{name}"))
        return permissions
