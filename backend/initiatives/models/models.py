import logging

from behaviors.models import Authored, Published, Timestamped
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.contrib.gis.db import models as geo_models
from django.core import validators
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from initiatives.utils import validate_file_extension
from simple_history.models import HistoricalRecords

logger = logging.getLogger(__name__)


class InitiativeType(models.TextChoices):
    BOTHERS_ME = "MM", _("MOTI ME!")
    HAVE_IDEA = "II", _("IMAM IDEJO!")
    INTERESTED_IN = "ZM", _("ZANIMA ME!")


class Reviwers(models.TextChoices):
    SUPER_ADMIN = "SA", _("SUPER ADMIN")
    AREA_ADMIN = "AA", _("AREA ADMIN")
    AREA_APPRAISER = "AP", _("AREA APPRAISER")
    CONTRACTOR_APPRAISER = "CA", _("CONTRACTOR APPRAISER")

    def get_order():
        return ["SA", "AA", "AP", "CA"]

    def get_role_url_key(key):
        return {"SA": "super", "AA": "area", "AP": "appraiser", "CA": "contractor"}[key]

    def role_to_str(role):
        if role == None:
            return ""
        return {
            "SA": _("Nivo 1"),
            "AA": _("Nivo 2"),
            "AP": _("Nivo 3"),
            "CA": _("Nivo 4"),
        }[role]


class CommentStatus(models.TextChoices):
    PUBLISHED = "PU", _("PUBLISHED")
    DELETED = "D", _("DELETED")
    # PENDING = 'PE', _('PENDING')


class NotificationType(models.TextChoices):
    NEW = "nw", _("NEW")
    UPDATED = "up", _("UPDATED")


class StatusInitiative(Timestamped, Published, Authored):
    initiative = models.ForeignKey(
        "initiatives.Initiative",
        verbose_name=_("Initiative"),
        related_name="initiative_statuses",
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        "Status",
        verbose_name=_("Status of initiative"),
        related_name="initiative_statuses",
        on_delete=models.CASCADE,
    )
    note = models.TextField(_("Note of status"), blank=True, null=True)
    email_content = models.TextField(_("Email response"), blank=True, null=True)
    reason_for_rejection = models.ForeignKey(
        "Rejection",
        null=True,
        blank=True,
        verbose_name=_("Rejection"),
        on_delete=models.SET_NULL,
    )
    competent_service = models.ForeignKey(
        "CompetentService",
        null=True,
        blank=True,
        verbose_name=_("CompetentService"),
        related_name="initiative_statuses",
        on_delete=models.CASCADE,
    )
    is_email_sent = models.BooleanField(_("Is email sent"), default=False)

    history = HistoricalRecords()

    def to_table_row(self):
        draft_style = (
            'style="background-color: coral;"'
            if self.draft
            else 'style="background-color: lightgreen;"'
        )
        return f'<tr><th>{self.status.name}</th><th>{self.note[:50] if self.note else ""}</th><th {draft_style}>{_("objavljeno") if self.published else _("osnutek")}</th><th>{self.created.date().isoformat() if self.created else 0}</th><th>{self.author.username}</th></tr>'

    def __str__(self):
        return f"{self.status.name}: {self.created}"

    class Meta:
        verbose_name = _("Status pobude")
        verbose_name_plural = _("Statusi pobude")


class ReviewerHistory(Timestamped):
    initiative = models.ForeignKey(
        "initiatives.Initiative",
        verbose_name=_("Initiative"),
        related_name="reviewer_history",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        "AllAdminUser",
        verbose_name=_("Reviewer"),
        related_name="reviewer_history",
        on_delete=models.CASCADE,
    )


class HearManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name="Slišimo")


class EditingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name="Urejamo")


class ProgressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name="V izvajanju")


class DoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name="Izvedeno")


class FinishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name="Zaključeno")


class RejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name="Zavrnjeno")


class StatusInitiativeHear(StatusInitiative):
    objects = HearManager()

    class Meta:
        proxy = True
        verbose_name = _("Status pobude slišimo")
        verbose_name_plural = _("Statusi pobude slišimo")

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name="Slišimo")
        return super().save(*args, **kwargs)


class StatusInitiativeEditing(StatusInitiative):
    objects = EditingManager()

    class Meta:
        proxy = True
        verbose_name = _("Status pobude urejamo")
        verbose_name_plural = _("Statusi pobude urejamo")

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name="Urejamo")
        return super().save(*args, **kwargs)


class StatusInitiativeProgress(StatusInitiative):
    objects = ProgressManager()

    class Meta:
        proxy = True
        verbose_name = _("Status pobude v izvajanju")
        verbose_name_plural = _("Statusi pobude v izvajanju")

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name="V izvajanju")
        return super().save(*args, **kwargs)


class StatusInitiativeFinished(StatusInitiative):
    objects = FinishedManager()

    class Meta:
        proxy = True
        verbose_name = _("Status pobude zaključeno")
        verbose_name_plural = _("Statusi pobude zaključeno")

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name="Zaključeno")
        return super().save(*args, **kwargs)


class StatusInitiativeDone(StatusInitiative):
    objects = DoneManager()

    class Meta:
        proxy = True
        verbose_name = _("Status pobude izvedeno")
        verbose_name_plural = _("Statusi pobude izvedeno")

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name="Izvedeno")
        return super().save(*args, **kwargs)


class StatusInitiativeRejected(StatusInitiative):
    objects = RejectedManager()

    class Meta:
        proxy = True
        verbose_name = _("Status pobude zavrnjeno")
        verbose_name_plural = _("Statusi pobude zavrnjeno")

    def save(self, *args, **kwargs):
        logger.warning(kwargs.keys())
        self.status = Status.objects.get(name="Zavrnjeno")
        return super().save(*args, **kwargs)


class Status(Timestamped):
    name = models.CharField(_("Status"), max_length=50)
    note = models.TextField(_("Default note of status"))
    default_email = models.TextField(_("Default email response"))

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statusi")


class Description(Timestamped):
    initiative = models.ForeignKey(
        "initiatives.Initiative",
        verbose_name=_("Initiative"),
        related_name="descriptions",
        on_delete=models.CASCADE,
    )
    field = models.CharField(_("Description type"), max_length=50)
    title = models.CharField(_("Description title"), max_length=1024)
    order = models.IntegerField(default=0)
    content = models.TextField(_("Description content"))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Opis")
        verbose_name_plural = _("Opisi")
        ordering = ["order"]


class Zone(Timestamped):
    name = models.CharField(_("Name of zone"), max_length=50)
    polygon = geo_models.PolygonField(_("Polygon of zone"))

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Območje")
        verbose_name_plural = _("Območja")


class CompetentService(Timestamped):
    name = models.CharField(_("Name of zone"), max_length=50)
    description = models.TextField(_("Description of service"))

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Comment(Timestamped, Authored):
    initiative = models.ForeignKey(
        "initiatives.Initiative",
        verbose_name=_("Initiative"),
        related_name="initiative_comments",
        on_delete=models.CASCADE,
    )
    content = models.TextField(_("Comment"))
    status = models.CharField(
        _("Comment status"),
        max_length=2,
        choices=CommentStatus.choices,
        default=CommentStatus.PUBLISHED,
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Komentar")
        verbose_name_plural = _("Komentarji")


class Vote(Timestamped, Authored):
    initiative = models.ForeignKey(
        "initiatives.Initiative",
        verbose_name=_("Initiative"),
        related_name="votes",
        on_delete=models.CASCADE,
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Glas")
        verbose_name_plural = _("Glasovi")


class User(AbstractUser, Timestamped):
    note = models.TextField(_("Note"), null=True, blank=True, default="")
    phone_number = models.CharField(
        _("Phone number"), max_length=50, null=True, blank=True
    )
    organizations = models.ManyToManyField(
        "Organization", blank=True, related_name="users", verbose_name=_("Organization")
    )
    zones = models.ManyToManyField(
        "Zone", blank=True, related_name="users", verbose_name=_("MČ/KS")
    )
    competent_services = models.ManyToManyField(
        "CompetentService",
        blank=True,
        related_name="users",
        verbose_name=_("Competent service"),
    )
    area = models.ManyToManyField(
        "Area", blank=True, related_name="users", verbose_name=_("Area")
    )
    role = models.CharField(
        _("Role"),
        max_length=2,
        choices=Reviwers.choices,
        default=None,
        null=True,
        blank=True,
    )
    email = models.EmailField(_("email address"), blank=False, unique=True)
    # a username field that allows a space
    username = models.CharField(
        _("username"),
        max_length=30,
        unique=True,
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and " "@/./+/-/_ only."
        ),
        validators=[
            validators.RegexValidator(
                r"^[\w.@+ -]+$", _("Enter a valid username."), "invalid"
            )
        ],
    )
    email_confirmed = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    blocked_email_sent = models.BooleanField(default=False)

    _old_note = None

    history = HistoricalRecords()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_note = self.note

    def __str__(self):
        return f"{self.username}: {Reviwers.role_to_str(self.role)}"

    class Meta:
        verbose_name = _("Uporabnik")
        verbose_name_plural = _("Uporabniki")


class SuperAdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Reviwers.SUPER_ADMIN)


class AllAdminManager(BaseUserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                role__in=[
                    Reviwers.SUPER_ADMIN,
                    Reviwers.AREA_ADMIN,
                    Reviwers.AREA_APPRAISER,
                    Reviwers.CONTRACTOR_APPRAISER,
                ]
            )
        )


class AllAdminUser(User):
    objects = AllAdminManager()

    class Meta:
        proxy = True
        verbose_name = _("All admin")
        verbose_name_plural = _("All admins")


class SuperAdminUser(User):
    objects = SuperAdminManager()

    class Meta:
        proxy = True
        verbose_name = _("Super admin")
        verbose_name_plural = _("Super admin")

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.is_staff = True
            self.role = Reviwers.SUPER_ADMIN
        return super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .exclude(
                Q(role=Reviwers.SUPER_ADMIN)
                | Q(role=Reviwers.AREA_ADMIN)
                | Q(role=Reviwers.AREA_APPRAISER)
                | Q(role=Reviwers.CONTRACTOR_APPRAISER)
            )
        )


class BasicUser(User):
    objects = UserManager()

    class Meta:
        proxy = True
        verbose_name = _("Basic user")
        verbose_name_plural = _("Basic users")


class AreaAdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Reviwers.AREA_ADMIN)


class AreaAdminUser(User):
    objects = AreaAdminManager()

    class Meta:
        proxy = True
        verbose_name = _("Admin področni")
        verbose_name_plural = _("Admini področni")

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.is_staff = True
            self.role = Reviwers.AREA_ADMIN
        return super().save(*args, **kwargs)


class AreaAppraiserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Reviwers.AREA_APPRAISER)


class AreaAppraiserUser(User):
    objects = AreaAppraiserManager()

    class Meta:
        proxy = True
        verbose_name = _("Cenilec področni")
        verbose_name_plural = _("Cenilci področni")

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.is_staff = True
            self.role = Reviwers.AREA_APPRAISER
        return super().save(*args, **kwargs)


class ContractorAppraiserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Reviwers.CONTRACTOR_APPRAISER)


class ContractorAppraiserUser(User):
    objects = ContractorAppraiserManager()

    class Meta:
        proxy = True
        verbose_name = _("Cenilec izvajalec")
        verbose_name_plural = _("Cenilci izvajalec")

    def save(self, *args, **kwargs):
        logger.warning("SAVE")
        if self.pk == None:
            self.is_staff = True
            self.role = Reviwers.CONTRACTOR_APPRAISER
        return super().save(*args, **kwargs)


class Organization(Timestamped):
    name = models.CharField(_("name"), max_length=50)
    number_of_members = models.IntegerField(_("Number of members"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Organizacija")
        verbose_name_plural = _("Organizacije")


class Area(Timestamped):
    name = models.CharField(_("Area name"), max_length=128)
    note = models.TextField(_("Notes"))
    competent_service = models.ForeignKey(
        "CompetentService",
        verbose_name=_("Competent service"),
        related_name="areas",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Področje")
        verbose_name_plural = _("Področja")


class Rejection(Timestamped):
    name = models.CharField(_("Name of rejection"), max_length=50)
    note = models.TextField(_("Note for rejection"))

    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Zavrnitev")
        verbose_name_plural = _("Zavrnitve")


class FAQ(Timestamped):
    question = models.TextField(_("question"))
    answer = models.TextField(_("answer"))
    order = models.IntegerField(_("Order"), default=1)

    history = HistoricalRecords()

    def __str__(self):
        return self.question[:50]

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")


class File(Timestamped):
    initiative = models.ForeignKey(
        "initiatives.Initiative",
        verbose_name=_("Initiative"),
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )
    status_initiative = models.ForeignKey(
        "StatusInitiative",
        verbose_name=_("Status Initiative"),
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )
    name = models.CharField(_("Display name"), max_length=50)
    file = models.FileField(
        _("File"), upload_to="files", validators=[validate_file_extension]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Datoteka")
        verbose_name_plural = _("Datoteke")


class Image(Timestamped):
    image = models.ImageField(_("Image"), upload_to="images", null=True, blank=True)
    name = models.CharField(_("Display name"), max_length=50, null=True, blank=True)

    def __str__(self):
        try:
            return self.image.url
        except:
            return "no image"

    class Meta:
        verbose_name = _("Slika")
        verbose_name_plural = _("Slike")


class DescriptionDefinition(Timestamped, Authored):
    type = models.CharField(
        _("Initiative type"),
        max_length=2,
        choices=InitiativeType.choices,
        default=InitiativeType.BOTHERS_ME,
    )
    order = models.IntegerField(default=0)
    field = models.CharField(_("Field name"), max_length=50)
    title = models.CharField(_("Title"), max_length=1024)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Razdelek opisa")
        verbose_name_plural = _("Razdeleki opisa")


class RestorePassword(Timestamped):
    user = models.ForeignKey(
        "User",
        verbose_name=_("User"),
        related_name="restore_passwords",
        on_delete=models.CASCADE,
    )
    key = models.CharField(_("key"), max_length=50)

    class Meta:
        verbose_name = _("Restore password")
        verbose_name_plural = _("Restore passwords")


class ConfirmEmail(Timestamped):
    user = models.ForeignKey(
        "User",
        verbose_name=_("User"),
        related_name="conform_emails",
        on_delete=models.CASCADE,
    )
    key = models.CharField(_("key"), max_length=50)

    class Meta:
        verbose_name = _("Confirm email")
        verbose_name_plural = _("Confirm emails")


class Notification(Timestamped):
    for_user = models.ForeignKey(
        "User",
        verbose_name=_("User"),
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    for_area = models.ForeignKey(
        "Area",
        verbose_name=_("Area"),
        related_name="notifications",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    type = models.CharField(
        _("Notification type"),
        max_length=2,
        choices=NotificationType.choices,
        default=NotificationType.NEW,
    )
    initiative = models.ForeignKey(
        "initiatives.Initiative",
        verbose_name=_("Initiative"),
        related_name="notifications",
        on_delete=models.CASCADE,
    )
    is_sent = models.BooleanField(_("is sent"), default=False)

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "created",
                    "is_sent",
                ]
            ),
        ]
        verbose_name = _("Obvestila")
        verbose_name_plural = _("Obvestila")


class Address(Timestamped):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = _("Naslov")
        verbose_name_plural = _("Naslovi")
