from django.db import models
from django.conf import settings
from django.utils.html import mark_safe
from django.utils.translation import gettext as _
from django.contrib.gis.db import models as geo_models
from django.urls import reverse

from simple_history.models import HistoricalRecords

from behaviors.models import Timestamped, Authored, Published

from initiatives.models import CommentStatus, InitiativeType, Reviwers, Zone

import logging
logger = logging.getLogger(__name__)

# This is used for showing admin all initialives which is asigned admins with lower permissions
# PERMISSIONS = {
#     None: [Reviwers.AREA_ADMIN, Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER],
#     Reviwers.AREA_ADMIN: [Reviwers.SUPER_ADMIN, Reviwers.AREA_ADMIN, Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER],
#     Reviwers.AREA_APPRAISER: [Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER],
#     Reviwers.CONTRACTOR_APPRAISER: [Reviwers.CONTRACTOR_APPRAISER],
# }
"""
Work around. That all admins will see the initiative when it is assigned to any role of admin.
"""
PERMISSIONS = {
    None: [Reviwers.SUPER_ADMIN, Reviwers.AREA_ADMIN, Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER],
    Reviwers.AREA_ADMIN: [Reviwers.SUPER_ADMIN, Reviwers.AREA_ADMIN, Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER],
    Reviwers.AREA_APPRAISER: [Reviwers.SUPER_ADMIN, Reviwers.AREA_ADMIN, Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER],
    Reviwers.CONTRACTOR_APPRAISER: [Reviwers.SUPER_ADMIN, Reviwers.AREA_ADMIN, Reviwers.AREA_APPRAISER, Reviwers.CONTRACTOR_APPRAISER],
}

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
        'initiatives.AllAdminUser',
        verbose_name=_('Reviewer'),
        related_name='reviewed',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    reviewer_user_history = models.ManyToManyField(
        'initiatives.AllAdminUser',
        verbose_name=_('Reviewer history'),
        through='initiatives.ReviewerHistory',
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
        verbose_name=_('Lokacija'),
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
        verbose_name=_('publisher'),
        related_name='published_initiatives',
        null=True,
        blank=True)
    cover_image = models.ForeignKey(
        'initiatives.Image',
        verbose_name=_('Cover image before'),
        on_delete=models.SET_NULL,
        related_name='initiative_before',
        null=True,
        blank=True)
    cover_image_after = models.ForeignKey(
        'initiatives.Image',
        verbose_name=_('Cover image after'),
        on_delete=models.SET_NULL,
        related_name='initiative_after',
        null=True,
        blank=True)
    archived = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Arhivirano',)
    is_draft = models.BooleanField(
        _('In review'),
        default=False)
    is_social_inovative_idea = models.BooleanField(
        _('Is social inovative idea'),
        default=False)

    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Pobuda")
        verbose_name_plural = _('Pobude')

    def __str__(self):
        return f'#{self.id} {self.title}' if self.title else f'#{self.id} unnamed'

    def comment_count(self):
        return self.initiative_comments.filter(status=CommentStatus.PUBLISHED).count()

    def tilte(self):
        return f'#{self.id} {self.title}' if self.title else f'#{self.id} unnamed'

    def status(self):
        try:
            return self.initiative_statuses.filter(publication_status=Published.PUBLISHED).latest('created').status.name
        except:
            return None

    def telephone(self):
        self.author.phone_number

    def email(self):
        self.author.email

    def status_history(self):
        statuses = self.initiative_statuses.all()
        if statuses:
            table_lines = "".join([status.to_table_row() for status in statuses.order_by('created')])
        else:
            table_lines = f'''<tr>
                <td colspan="4">{_("Pobuda je brez statusa")}</td>
                </tr>'''

        return mark_safe(
            f'''<table>
            <tr>
                <th>{_("Status")}</th>
                <th>{_("Opis")}</th>
                <th>{_("Status objace")}</th>
                <th>{_("Status spremenjen dne")}</th>
                <th>{_("Avtor")}</th>
            </tr>
                {table_lines}
            </table>
            '''
            )

    def description(self):
        output = ''
        descriptions = self.descriptions.all()
        for description in descriptions:
            output += f'<h3>{description.title}</h3><br>{description.content}'

        return mark_safe(output)

    def images_preview(self):
        images = ""
        if self.cover_image:
            images += f'''<img src="{self.cover_image}" style="width:50%;">'''
        if self.cover_image_after:
            images += f'''<img src="{self.cover_image_after}" style="width:50%;">'''
        return mark_safe(
            f'''
            <div style="width:100%;">
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

    def get_admin_url(self, role):
        role_str = self.get_role_url_key(role)
        type_str = self.get_type_url_key(self.type)
        logger.debug(f'admin:{type_str}initiative{role_str}_change')
        return reverse(f'admin:initiatives_{type_str}initiative{role_str}_change',  args=[self.id] )

    def get_role_url_key(self, key):
        return {
            'SA': 'super',
            'AA': 'area',
            'AP': 'appraiser',
            'CA': 'contractor'
            }[key]

    def get_type_url_key(self, key):
        return {
            InitiativeType.BOTHERS_ME : 'bothers',
            InitiativeType.HAVE_IDEA: 'idea',
            InitiativeType.INTERESTED_IN: 'interested'

        }[key]

    _needs_publish.boolean = True
    _is_published.boolean = True
    is_published = property(_is_published)
    needs_published = property(_needs_publish)

    _is_published.short_description = _("Objavleno")
    _needs_publish.short_description = _("Potrebuje pregled")
    comment_count.short_description = _("Št. komentarjev")
    status_history.short_description = _("Zgodovina statusov")
    images_preview.short_description = _("Predogled slik")
    description.short_description = _("Opis")


class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(archived__isnull=False)


class ArchivedInitiative(Initiative):
    objects = ArchivedManager()
    class Meta:
        proxy=True
        verbose_name = _("Arhivirana pobuda")
        verbose_name_plural = _('Arhivirane pobude')

# MOTI ME
class BothersManager(models.Manager):
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        if self.reviewer:
            return super().get_queryset().filter(type=InitiativeType.BOTHERS_ME, archived=None, reviewer__in=PERMISSIONS[self.reviewer], is_draft=False)
        else:
            return super().get_queryset().filter(type=InitiativeType.BOTHERS_ME, archived=None, is_draft=False)


class BothersInitiativeSuper(Initiative):
    objects = BothersManager(None)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda moti me (superadmin)")
        verbose_name_plural = _('Pobude moti me (superadmin)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativesuper_change',  args=[self.id])


class BothersInitiativeArea(Initiative):
    objects = BothersManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda moti me (admin področni)")
        verbose_name_plural = _('Pobude moti me (admin področni)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativearea_change',  args=[self.id] )


class BothersInitiativeAppraiser(Initiative):
    objects = BothersManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda moti me (cenilec področni)")
        verbose_name_plural = _('Pobude moti me (cenilci področni)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativeappraiser_change',  args=[self.id] )


class BothersInitiativeContractor(Initiative):
    objects = BothersManager(Reviwers.CONTRACTOR_APPRAISER)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda moti me (cenilec izvajalec)")
        verbose_name_plural = _('Pobude moti me (cenilci izvajalci)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_bothersinitiativecontractor_change',  args=[self.id] )


# IMAM IDEJO
class IdeaManager(models.Manager):
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        if self.reviewer:
            return super().get_queryset().filter(type=InitiativeType.HAVE_IDEA, archived=None, reviewer__in=PERMISSIONS[self.reviewer], is_draft=False)
        else:
            return super().get_queryset().filter(type=InitiativeType.HAVE_IDEA, archived=None, is_draft=False)


class IdeaInitiativeSuper(Initiative):
    objects = IdeaManager(None)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda imam idejo (superadmin)")
        verbose_name_plural = _('Pobude imam idejo (superadmin)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativesuper_change',  args=[self.id] )


class IdeaInitiativeArea(Initiative):
    objects = IdeaManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda imam idejo (admin področni)")
        verbose_name_plural = _('Pobude imam idejo (admin področni)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativearea_change',  args=[self.id] )


class IdeaInitiativeAppraiser(Initiative):
    objects = IdeaManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda imam idejo (cenilec področni)")
        verbose_name_plural = _('Pobude imam idejo (cenilec področni)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativeappraiser_change',  args=[self.id] )


class IdeaInitiativeContractor(Initiative):
    objects = IdeaManager(Reviwers.CONTRACTOR_APPRAISER)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda imam idejo (cenilec izvajalec)")
        verbose_name_plural = _('Pobude imam idejo (cenilec izvajalec)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_ideainitiativecontractor_change',  args=[self.id] )


# ZANIMA ME
class InterestedManager(models.Manager): # zanima me
    def __init__(self, reviewer):
        self.reviewer = reviewer
        super().__init__()
    def get_queryset(self):
        if self.reviewer:
            return super().get_queryset().filter(type=InitiativeType.INTERESTED_IN, archived=None, reviewer__in=PERMISSIONS[self.reviewer], is_draft=False)
        else:
            return super().get_queryset().filter(type=InitiativeType.INTERESTED_IN, archived=None, is_draft=False)


class InterestedInitiativeSuper(Initiative):
    objects = InterestedManager(None)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda zanima me (superadmin)")
        verbose_name_plural = _('Pobude zanima me (superadmin)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_interestedinitiativesuper_change',  args=[self.id] )


class InterestedInitiativeArea(Initiative):
    objects = InterestedManager(Reviwers.AREA_ADMIN)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda zanima me (admin področni)")
        verbose_name_plural = _('Pobude zanima me (admin področni)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_interestedinitiativearea_change',  args=[self.id] )


class InterestedInitiativeAppraiser(Initiative):
    objects = InterestedManager(Reviwers.AREA_APPRAISER)
    class Meta:
        proxy=True
        verbose_name = _("Pobuda zanima me (cenilec področni)")
        verbose_name_plural = _('Pobude zanima me (cenilec področni)')

    def get_admin_change_url(self):
        return reverse('admin:initiatives_interestedinitiativeappraiser_change',  args=[self.id] )
