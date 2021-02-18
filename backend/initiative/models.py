from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.gis.db import models as geo_models

from behaviors.behaviors import Timestamped, Authored

from initiatives.models import CommentStatus, InitiativeType


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


class BothersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=InitiativeType.BOTHERS_ME)


class BothersInitiative(Initiative):
    objects = BothersManager()
    class Meta:
        proxy=True


class IdeaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=InitiativeType.HAVE_IDEA)


class IdeaInitiative(Initiative):
    objects = IdeaManager()
    class Meta:
        proxy=True


class InterestedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=InitiativeType.INTERESTED_IN)


class InterestedInitiative(Initiative):
    objects = InterestedManager()
    class Meta:
        proxy=True


