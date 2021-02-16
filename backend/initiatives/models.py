from django.db import models
from django.contrib.gis.db import models as geo_models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from django.core import validators

from behaviors.behaviors import Timestamped, Authored


# TODO o izboljšamo maribor naredi podobno kot je na mauticu.
# Elementi novice so lahko [video, slika, text, naslov...?], na seznamu lahko urejaš vrstni red.

class InitiativeType(models.TextChoices):
    BOTHERS_ME = 'MM', _('MOTI ME!')
    HAVE_IDEA = 'II', _('IMAM IDEJO!')
    INTERESTED_IN = 'ZM', _('ZANIMA ME!')


class CommentStatus(models.TextChoices):
    PUBLISHED = 'PU', 'PUBLISHED'
    DELETED = 'D', 'DELETED'
    PENDING = 'PE', 'PENDING'


class Initiative(Timestamped, Authored):
    type = models.CharField(
        _('Initiative type'),
        max_length=2,
        choices=InitiativeType.choices,
        default=InitiativeType.BOTHERS_ME)
    title = models.CharField(
        _('Title'),
        max_length=50)
    statuses = models.ManyToManyField(
        'Status',
        verbose_name=_('Status of initiative'),
        through='StatusInitiative')
    area = models.ForeignKey(
        'Area',
        verbose_name=_('Area'),
        on_delete=models.CASCADE,
        related_name='initiatives')
    location = geo_models.PointField()
    address = models.CharField(
        _("Address of initiative"),
        max_length=100)
    zone = models.ForeignKey(
        'Zone',
        verbose_name=_('GEO Zone of initiative'),
        on_delete=models.CASCADE,
        related_name='initiatives')
    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='published_initiatives',
        null=True,
        blank=True)
    cover_image = models.ForeignKey(
        'Image',
        verbose_name=_('Cover image before'),
        on_delete=models.CASCADE,
        related_name='initiative_before',
        null=True,
        blank=True)
    cover_image_after = models.ForeignKey(
        'Image',
        verbose_name=_('Cover image after'),
        on_delete=models.CASCADE,
        related_name='initiative_after',
        null=True,
        blank=True)
    archived = models.DateTimeField(
        null=True,
        blank=True)
    in_review = models.BooleanField(
        _('In review'),
        default=False)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.initiative_comments.filter(status=CommentStatus.PUBLISHED).count()

    def status(self):
        try:
            return self.initiative_statuses.latest('created').status.name
        except:
            return None

    def vote_count(self):
        return self.votes.count()

    def is_archived(self):
        return self.archived is not None

    def archive(self, *args, **kwargs):
        if not self.pk:
            raise ObjectDoesNotExist(
                _('Object must be created before it can be archived'))
        self.archived = timezone.now()
        return super(StoreDeleted, self).save(*args, **kwargs)


class StatusInitiative(Timestamped):
    initiative = models.ForeignKey(
        'Initiative',
        verbose_name=_('Initiative'),
        related_name='initiative_statuses',
        on_delete=models.CASCADE)
    status = models.ForeignKey(
        'Status',
        verbose_name=_('Status of initiative'),
        related_name='initiative_statuses',
        on_delete=models.CASCADE)
    note = models.TextField(
        _('Note of status'))
    email_content = models.TextField(
        _('Email response'))
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


class StatusInitiativeEditing(StatusInitiative):
    objects = EditingManager()
    class Meta:
        proxy=True


class StatusInitiativeProgress(StatusInitiative):
    objects = ProgressManager()
    class Meta:
        proxy=True


class StatusInitiativeFinished(StatusInitiative):
    objects = FinishedManager()
    class Meta:
        proxy=True


class StatusInitiativeDone(StatusInitiative):
    objects = DoneManager()
    class Meta:
        proxy=True


class StatusInitiativeRejected(StatusInitiative):
    objects = RejectedManager()
    class Meta:
        proxy=True


class Status(Timestamped):
    name = models.CharField(_('Status'), max_length=50)
    note = models.TextField(_('Default note of status'))
    default_email = models.TextField(_('Default email response'))

    def __str__(self):
        return self.name


class Description(Timestamped):
    initiative = models.ForeignKey(
        'Initiative',
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
        'Initiative',
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
        'Initiative',
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
    # a username field that allows a space
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+ -]+$', _('Enter a valid username.'), 'invalid')
        ])


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
        max_length=50)
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
        'Initiative',
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
        max_length=100)

    def __str__(self):
        return self.name


class Image(Timestamped):
    image = models.ImageField(
        _('Image'),
        upload_to='images',
        null=True,
        blank=True)
    def __str__(self):
        return self.name
