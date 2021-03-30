from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core import validators
from django.contrib.gis.db import models as geo_models
from django.contrib.auth.models import Group

from behaviors.behaviors import Timestamped, Authored, Published

from initiatives.utils import validate_file_extension

import logging
logger = logging.getLogger(__name__)


class InitiativeType(models.TextChoices):
    BOTHERS_ME = 'MM', _('MOTI ME!')
    HAVE_IDEA = 'II', _('IMAM IDEJO!')
    INTERESTED_IN = 'ZM', _('ZANIMA ME!')


class Reviwers(models.TextChoices):
    SUPER_ADMIN = 'SA', _('SUPER ADMIN')
    AREA_ADMIN = 'AA', _('AREA ADMIN')
    AREA_APPRAISER = 'AP', _('AREA APPRAISER')
    CONTRACTOR_APPRAISER = 'CA', _('CONTRACTOR APPRAISER')

    def get_order():
        return ['SA', 'AA', 'AP', 'CA']


class CommentStatus(models.TextChoices):
    PUBLISHED = 'PU', 'PUBLISHED'
    DELETED = 'D', 'DELETED'
    PENDING = 'PE', 'PENDING'


class StatusInitiative(Timestamped, Published):
    initiative = models.ForeignKey(
        'initiatives.Initiative',
        verbose_name=_('Initiative'),
        related_name='initiative_statuses',
        on_delete=models.CASCADE)
    status = models.ForeignKey(
        'Status',
        verbose_name=_('Status of initiative'),
        related_name='initiative_statuses',
        on_delete=models.CASCADE)
    note = models.TextField(
        _('Note of status'),
        blank=True,
        null=True)
    email_content = models.TextField(
        _('Email response'),
        blank=True,
        null=True)
    reason_for_rejection = models.ForeignKey(
        'Rejection',
        null=True,
        blank=True,
        verbose_name=_('Rejection'),
        on_delete=models.SET_NULL)
    competent_service = models.ForeignKey(
        'CompetentService',
        null=True,
        blank=True,
        verbose_name=_('CompetentService'),
        related_name='initiative_statuses',
        on_delete=models.CASCADE)
    is_email_sent = models.BooleanField(
        _("Is email sent"),
        default=False)

    def to_table_row(self):
        draft_style = 'style="background-color: coral;"' if self.draft else 'style="background-color: lightgreen;"'
        return f'<tr><th>{self.status.name}</th><th>{self.note[:50] if self.note else ""}</th><th {draft_style}>{_("published") if self.published else _("draft")}</th><th>{self.created.date().isoformat() if self.created else 0}</th></tr>'

class HearManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name='Slišimo')


class EditingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name='Urejamo')


class ProgressManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name='V izvajanju')


class DoneManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name='Izvedeno')


class FinishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name='Zaključeno')


class RejectedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status__name='Zavrnjeno')


class StatusInitiativeHear(StatusInitiative):
    objects = HearManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name='Slišimo')
        return super().save(*args, **kwargs)


class StatusInitiativeEditing(StatusInitiative):
    objects = EditingManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name='Urejamo')
        return super().save(*args, **kwargs)


class StatusInitiativeProgress(StatusInitiative):
    objects = ProgressManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name='V izvajanju')
        return super().save(*args, **kwargs)


class StatusInitiativeFinished(StatusInitiative):
    objects = FinishedManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name='Zaključeno')
        return super().save(*args, **kwargs)


class StatusInitiativeDone(StatusInitiative):
    objects = DoneManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name='Izvedeno')
        return super().save(*args, **kwargs)


class StatusInitiativeRejected(StatusInitiative):
    objects = RejectedManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        self.status = Status.objects.get(name='Zavrnjeno')
        return super().save(*args, **kwargs)


class Status(Timestamped):
    name = models.CharField(_('Status'), max_length=50)
    note = models.TextField(_('Default note of status'))
    default_email = models.TextField(_('Default email response'))

    def __str__(self):
        return self.name


class Description(Timestamped):
    initiative = models.ForeignKey(
        'initiatives.Initiative',
        verbose_name=_('Initiative'),
        related_name='descriptions',
        on_delete=models.CASCADE)
    field = models.CharField(
        _('Description type'),
        max_length=50)
    title =  models.CharField(
        _('Description title'),
        max_length=100)
    order = models.IntegerField(default=0)
    content = models.TextField(
        _('Description content'))


class Zone(Timestamped):
    name = models.CharField(_('Name of zone'), max_length=50)
    polygon = geo_models.PolygonField(_('Polygon of zone'))

    def __str__(self):
        return self.name


class CompetentService(Timestamped):
    name = models.CharField(_('Name of zone'), max_length=50)
    description = models.TextField(_('Description of service'))

    def __str__(self):
        return self.name


class Comment(Timestamped, Authored):
    initiative = models.ForeignKey(
        'initiatives.Initiative',
        verbose_name=_('Initiative'),
        related_name='initiative_comments',
        on_delete=models.CASCADE)
    content = models.TextField(
        _('Comment'))
    status = models.CharField(
        _('Comment status'),
        max_length=2,
        choices=CommentStatus.choices,
        default=CommentStatus.PENDING)


class Vote(Timestamped, Authored):
    initiative = models.ForeignKey(
        'initiatives.Initiative',
        verbose_name=_('Initiative'),
        related_name='votes',
        on_delete=models.CASCADE)


class User(AbstractUser, Timestamped):
    note = models.TextField(
        _('Note'),
        null=True,
        blank=True,
        default='')
    phone_number = models.CharField(
        _('Phone number'),
        max_length=50,
        null=True,
        blank=True)
    organizations = models.ManyToManyField(
        'Organization',
        blank=True,
        related_name='users',
        verbose_name=_('Organization'))
    zones = models.ManyToManyField(
        'Zone',
        blank=True,
        related_name='users',
        verbose_name=_('MČ/KS'))
    competent_services = models.ManyToManyField(
        'CompetentService',
        blank=True,
        related_name='users',
        verbose_name=_('Competent service'))
    area = models.ManyToManyField(
        'Area',
        blank=True,
        related_name='users',
        verbose_name=_('Area'))
    role = models.CharField(
        _('Role'),
        max_length=2,
        choices=Reviwers.choices,
        default=None,
        null=True,
        blank=True)
    # a username field that allows a space
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+ -]+$', _('Enter a valid username.'), 'invalid')
        ])
    email_confirmed = models.BooleanField(default=False)


class SuperAdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Reviwers.SUPER_ADMIN)


class SuperAdminUser(User):
    objects = SuperAdminManager()
    class Meta:
        proxy=True

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.is_staff = True
            self.role = Reviwers.SUPER_ADMIN
        return super().save(*args, **kwargs)


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().exclude(
            Q(role=Reviwers.SUPER_ADMIN) |
            Q(role=Reviwers.AREA_ADMIN) |
            Q(role=Reviwers.AREA_APPRAISER) |
            Q(role=Reviwers.CONTRACTOR_APPRAISER))


class BasicUser(User):
    objects = UserManager()
    class Meta:
        proxy=True


class AreaAdminManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=Reviwers.AREA_ADMIN)


class AreaAdminUser(User):
    objects = AreaAdminManager()
    class Meta:
        proxy=True

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
        proxy=True

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
        proxy=True

    def save(self, *args, **kwargs):
        logger.warning('SAVE')
        if self.pk == None:
            self.is_staff = True
            self.role = Reviwers.CONTRACTOR_APPRAISER
        return super().save(*args, **kwargs)


class Organization(Timestamped):
    name = models.CharField(
        _('name'),
        max_length=50)
    number_of_members = models.IntegerField(
        _('Number of members'))

    def __str__(self):
        return self.name


class Area(Timestamped):
    name = models.CharField(
        _('Area name'),
        max_length=128)
    note = models.TextField(
        _('Notes'))
    competent_service = models.ForeignKey(
        'CompetentService',
        verbose_name=_('Competent service'),
        related_name='areas',
        on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Rejection(Timestamped):
    name = models.CharField(
        _('Name of rejection'),
        max_length=50)
    note = models.TextField(
        _('Note for rejection'))

    def __str__(self):
        return self.name


class FAQ(Timestamped):
    question = models.TextField(_('question'))
    answer = models.TextField(_('answer'))
    order = models.IntegerField(_("Order"), default=1)

    def __str__(self):
        return self.question[:50]


class File(Timestamped):
    initiative = models.ForeignKey(
        'initiatives.Initiative',
        verbose_name=_('Initiative'),
        on_delete=models.CASCADE,
        related_name='files',
        null=True,
        blank=True)
    status_initiative = models.ForeignKey(
        'StatusInitiative',
        verbose_name=_('Status Initiative'),
        on_delete=models.CASCADE,
        related_name='files',
        null=True,
        blank=True)
    name = models.CharField(
        _('Display name'),
        max_length=50)
    file = models.FileField(
        _('File'),
        upload_to='files',
        validators=[validate_file_extension])

    def __str__(self):
        return self.name


class Image(Timestamped):
    image = models.ImageField(
        _('Image'),
        upload_to='images',
        null=True,
        blank=True)
    name = models.CharField(
        _('Display name'),
        max_length=50,
        null=True,
        blank=True)

    def __str__(self):
        try:
            return self.image.url
        except:
            return 'no image'


class DescriptionDefinition(Timestamped, Authored):
    type = models.CharField(
        _('Initiative type'),
        max_length=2,
        choices=InitiativeType.choices,
        default=InitiativeType.BOTHERS_ME)
    order = models.IntegerField(default=0)
    field = models.CharField(
        _('Field name'),
        max_length=50)
    title = models.CharField(
        _('Title'),
        max_length=100)


class RestorePassword(Timestamped):
    user = models.ForeignKey(
        'User',
        verbose_name=_('User'),
        related_name='restore_passwords',
        on_delete=models.CASCADE)
    key = models.CharField(
        _('Description type'),
        max_length=50)


class ConfirmEmail(Timestamped):
    user = models.ForeignKey(
        'User',
        verbose_name=_('User'),
        related_name='conform_emails',
        on_delete=models.CASCADE)
    key = models.CharField(
        _('Description type'),
        max_length=50)

