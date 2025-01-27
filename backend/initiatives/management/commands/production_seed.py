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

    def handle(self, *args, **options):
        self.basc_options = [("change_", "Can change "), ("view_", "Can view ")]
        self.options = [
            ("add_", "Can add "),
            ("change_", "Can change "),
            ("view_", "Can view "),
        ]
        self.read = [("view_", "Can view ")]

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
        ct = ContentType.objects.get_for_model(models.AllAdminUser)
        permissions = self.get_permissions("alladminuser", ct, self.basc_options)
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

        ct = ContentType.objects.get_for_model(models.AreaAdminUser)
        permissions = self.get_permissions("areaadminuser", ct, self.read)
        admin_group.permissions.add(*permissions)
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

        user = models.User(
            first_name="Auth user",
            username="auth",
            is_active=True,
        )
        user.save()
        Application(
            client_id="kIZWxeodL29mfaKSIGQWPUuuck8CXv3m58XuJ8Y7",
            client_secret="54pWmrpj1y9FiwkUDofjeP4B5tbLQ4wW6F2wqsMT3JuQN4ApIqcveKlzOC1laQIJp8JpVi99EheHCkumEJ0o81J9f2uHK3eXjUdxprzDnWlsTuZM6cgv1Eo35KSr7Mfg",
            user=user,
            client_type="confidential",
            authorization_grant_type="password",
            name="client",
        ).save()

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
                name=a,
                note="Napisi opis",
            )
            area.save()

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

        models.DescriptionDefinition(
            order=1,
            type=models.InitiativeType.HAVE_IDEA,
            title="Na kratko opišite svojo pobudo oziroma predlog? Zakaj ta predlog? Katere izzive /probleme, pomankljivosti, slabosti v skupnosti/ mestu bi z uresničitvijo  vaše pobude rešili? ",
            field="title1",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=2,
            type=models.InitiativeType.HAVE_IDEA,
            title="Kakšen je vaš idejni predlog rešitve, izzivov/problemov, uvedbe izboljšav, izkoriščanja priložnosti? Kaj konkretno predlagate?  Kakšne priložnosti naslavlja?  Kaj bi se z izvedbo vašega predloga izboljšalo? Ali predlog spodbuja povezovanje /sodelovanje ljudi? Krepi njihove sposobnosti za lažje samostojno reševanje izzivov v skupnosti/mestu?",
            field="title2",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=3,
            type=models.InitiativeType.HAVE_IDEA,
            title="Kako in kje bi realizirali vašo pobudo-idejo? Katere aktivnosti (koraki /postopki, dela, opravila) so potrebni za izvedbo rešitve? Ali se lahko vaša pobuda realizira v nevladnem sektorju (v okviru društev, civilnih pobud ..), kot socialno podjetniški/zadružni/ podjetniški podjem, razvojni projekt v mestu ali kot gospodarski projekt/pobuda? Koga bi pritegnili k sodelovanju?",
            field="title3",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=4,
            type=models.InitiativeType.HAVE_IDEA,
            title="Ali lahko ocenite vrednost realizacije projekta / ideje (v EUR)?",
            field="title4",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=1,
            type=models.InitiativeType.BOTHERS_ME,
            title="Na kratko opišite, kaj vas moti. Zakaj? Če je mogoče, opišite svojo izkušnje, da nam pomagate bolje razumeti vašo pripombo.",
            field="title1",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=2,
            type=models.InitiativeType.BOTHERS_ME,
            title="Kako bi lahko to, kar vas moti, popravili?",
            field="title2",
            author_id=1,
        ).save()
        models.DescriptionDefinition(
            order=1,
            type=models.InitiativeType.INTERESTED_IN,
            title="Kaj vas zanima? Vaše vprašanje naj bo jasno in nedvoumno; če je potrebno in če je mogoče, na kratko opišite okoliščine, na katere se nanaša vaše vprašanje. Tako vam bomo lažje podali kvaliteten in konkreten odgovor.",
            field="title1",
            author_id=1,
        ).save()

    def get_permissions(self, name, ct, options=basc_options):
        permissions = []
        for option in options:
            print(f"{option[0]}{name}")
            permissions.append(Permission.objects.get(codename=f"{option[0]}{name}"))
        return permissions
