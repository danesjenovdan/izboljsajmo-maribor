from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from django.contrib.gis.db import models as geo_models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse

from behaviors.behaviors import Timestamped, Authored, Published

from initiatives.models import CommentStatus, InitiativeType, Reviwers, Zone


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
        default=Reviwers.AREA_ADMIN,)
    reviewer_user = models.ForeignKey(
        'initiatives.User',
        verbose_name=_('Reviewer'),
        related_name='reviewed',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    title = models.CharField(
        _('Title'),
        max_length=50,
        null=True,
        blank=True)
    statuses = models.ManyToManyField(
        'initiatives.Status',
        verbose_name=_('Status of initiative'),
        through='initiatives.StatusInitiative')
    area = models.ForeignKey(
        'initiatives.Area',
        verbose_name=_('Area'),
        on_delete=models.CASCADE,
        related_name='initiatives',
        null=True,
        blank=True)
    location = geo_models.PointField(
        null=True,
        blank=True)
    address = models.CharField(
        _("Address of initiative"),
        max_length=100,
        null=True,
        blank=True)
    zone = models.ForeignKey(
        'initiatives.Zone',
        verbose_name=_('GEO Zone of initiative'),
        on_delete=models.SET_NULL,
        related_name='initiatives',
        null=True,
        blank=True)
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
                {"".join([status.to_table_row() for status in self.initiative_statuses.all().order_by('created')])}
            </table>
            '''
            )

    def images_preview(self):
        images = ""
        if self.cover_image:
            images += f'''<img src="{self.cover_image}" style"width=25%;">'''
        if self.cover_image_after:
            images += f'''<img src="{self.cover_image_after}" style"width=25%;">'''
        return mark_safe(
            f'''
            <div style"width=50%;">
                {images}
            </div>
            '''
        )

    def _is_published(self):
        return bool(self.initiative_statuses.filter(publication_status=Published.PUBLISHED))

    def _needs_publish(self):
        return bool(self.initiative_statuses.filter(publication_status=Published.DRAFT))

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

    _needs_publish.boolean = True
    _is_published.boolean = True
    is_published = property(_is_published)
    needs_published = property(_needs_publish)


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
        if self.reviewer:
            return super().get_queryset().filter(type=InitiativeType.BOTHERS_ME, archived=None, reviewer=self.reviewer)
        else:
            return super().get_queryset().filter(type=InitiativeType.BOTHERS_ME, archived=None)


class BothersInitiativeSuper(Initiative):
    objects = BothersManager(None)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativesuper_change',  args=[self.id] )


class BothersInitiativeArea(Initiative):
    objects = BothersManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativearea_change',  args=[self.id] )


class BothersInitiativeAppraiser(Initiative):
    objects = BothersManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativeappraiser_change',  args=[self.id] )


class BothersInitiativeContractor(Initiative):
    objects = BothersManager(Reviwers.CONTRACTOR_APPRAISER)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativecontractor_change',  args=[self.id] )


# IMAM IDEJO
class IdeaManager(models.Manager):
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        if self.reviewer:
            return super().get_queryset().filter(type=InitiativeType.HAVE_IDEA, archived=None, reviewer=self.reviewer)
        else:
            return super().get_queryset().filter(type=InitiativeType.HAVE_IDEA, archived=None)


class IdeaInitiativeSuper(Initiative):
    objects = IdeaManager(None)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativesuper_change',  args=[self.id] )


class IdeaInitiativeArea(Initiative):
    objects = IdeaManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativearea_change',  args=[self.id] )


class IdeaInitiativeAppraiser(Initiative):
    objects = IdeaManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativeappraiser_change',  args=[self.id] )


class IdeaInitiativeContractor(Initiative):
    objects = IdeaManager(Reviwers.CONTRACTOR_APPRAISER)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativecontractor_change',  args=[self.id] )


# ZANIMA ME
class InterestedManager(models.Manager): # zanima me
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        if self.reviewer:
            return super().get_queryset().filter(type=InitiativeType.INTERESTED_IN, archived=None, reviewer=self.reviewer)
        else:
            return super().get_queryset().filter(type=InitiativeType.INTERESTED_IN, archived=None)


class InterestedInitiativeSuper(Initiative):
    objects = InterestedManager(None)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_interestedinitiativesuper_change',  args=[self.id] )


class InterestedInitiativeArea(Initiative):
    objects = InterestedManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_interestedinitiativearea_change',  args=[self.id] )


class InterestedInitiativeAppraiser(Initiative):
    objects = InterestedManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True

    def get_admin_change_url(self):
        return reverse('admin:initiatives_interestedinitiativeappraiser_change',  args=[self.id] )
