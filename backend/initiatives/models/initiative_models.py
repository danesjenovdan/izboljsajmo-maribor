from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from django.contrib.gis.db import models as geo_models
from django.db.models.signals import pre_save, post_save

from behaviors.behaviors import Timestamped, Authored

from initiatives.models import CommentStatus, InitiativeType, Reviwers


class Initiative(Timestamped, Authored):
    type = models.CharField(
        _('Initiative type'),
        max_length=2,
        choices=InitiativeType.choices,
        default=InitiativeType.BOTHERS_ME)
    reviewer = models.CharField(
        _('Reviewer role'),
        max_length=2,
        choices=Reviwers.choices,
        default=Reviwers.AREA_ADMIN)
    reviewer_user = models.ForeignKey(
        'initiatives.User',
        verbose_name=_('Reviewer'),
        related_name='reviewed',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    title = models.CharField(
        _('Title'),
        max_length=50)
    statuses = models.ManyToManyField(
        'initiatives.Status',
        verbose_name=_('Status of initiative'),
        through='initiatives.StatusInitiative')
    area = models.ForeignKey(
        'initiatives.Area',
        verbose_name=_('Area'),
        on_delete=models.CASCADE,
        related_name='initiatives')
    location = geo_models.PointField(default='POINT(0.0 0.0)')
    address = models.CharField(
        _("Address of initiative"),
        max_length=100)
    zone = models.ForeignKey(
        'initiatives.Zone',
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
        'initiatives.Image',
        verbose_name=_('Cover image before'),
        on_delete=models.CASCADE,
        related_name='initiative_before',
        null=True,
        blank=True)
    cover_image_after = models.ForeignKey(
        'initiatives.Image',
        verbose_name=_('Cover image after'),
        on_delete=models.CASCADE,
        related_name='initiative_after',
        null=True,
        blank=True)
    archived = models.DateTimeField(
        null=True,
        blank=True)
    is_draft = models.BooleanField(
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

    def status_history(self):
        return mark_safe(
            f'''<table>
            <tr>
                <th>{_("Status")}</th>
                <th>{_("Note")}</th>
                <th>{_("Published status")}</th>
                <th>{_("Status changed at")}</th>
            </tr>
                {"".join([status.to_table_row() for status in self.initiative_statuses.all()])}
            </table>
            '''
            )

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


class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived__isnull=False)


class ArchivedInitiative(Initiative):
    objects = ArchivedManager()
    class Meta:
        proxy=True

# MOTI ME
class BothersManager(models.Manager):
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        return super().get_queryset().filter(type=InitiativeType.BOTHERS_ME, archived=None, reviewer=self.reviewer)


class BothersInitiativeSuper(Initiative):
    objects = BothersManager(Reviwers.SUPER_ADMIN)
    class Meta:
        proxy=True


class BothersInitiativeArea(Initiative):
    objects = BothersManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True


class BothersInitiativeAppraiser(Initiative):
    objects = BothersManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True


class BothersInitiativeContractor(Initiative):
    objects = BothersManager(Reviwers.CONTRACTOR_APPRAISER)
    class Meta:
        proxy=True


# IMAM IDEJO
class IdeaManager(models.Manager):
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        return super().get_queryset().filter(type=InitiativeType.HAVE_IDEA, archived=None, reviewer=self.reviewer)


class IdeaInitiativeSuper(Initiative):
    objects = IdeaManager(Reviwers.SUPER_ADMIN)
    class Meta:
        proxy=True


class IdeaInitiativeArea(Initiative):
    objects = IdeaManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True


class IdeaInitiativeAppraiser(Initiative):
    objects = IdeaManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True


class IdeaInitiativeContractor(Initiative):
    objects = IdeaManager(Reviwers.CONTRACTOR_APPRAISER)
    class Meta:
        proxy=True


# ZANIMA ME
class InterestedManager(models.Manager): # zanima me
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        return super().get_queryset().filter(type=InitiativeType.INTERESTED_IN, archived=None, reviewer=self.reviewer)


class InterestedInitiativeSuper(Initiative):
    objects = InterestedManager(Reviwers.SUPER_ADMIN)
    class Meta:
        proxy=True


class InterestedInitiativeArea(Initiative):
    objects = InterestedManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True


class InterestedInitiativeAppraiser(Initiative):
    objects = InterestedManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True
