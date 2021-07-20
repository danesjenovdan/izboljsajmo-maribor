from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.contrib.admin import SimpleListFilter
from django.contrib.gis import admin as gis_admin
from django.db.models import Q
from django.utils.translation import gettext as _
from behaviors.models import Published

from initiatives.models import (
    Initiative, BothersInitiativeSuper, BothersInitiativeArea, BothersInitiativeAppraiser, BothersInitiativeContractor,
    IdeaInitiativeSuper, IdeaInitiativeArea, IdeaInitiativeAppraiser, IdeaInitiativeContractor,
    InterestedInitiativeSuper, InterestedInitiativeArea, InterestedInitiativeAppraiser,
    ArchivedInitiative, User, Reviwers
)

from initiatives.admin.admin import (DescriptionInline, FileInline, StatusInitiativeHearInline, StatusInitiativeEditingInline,
    StatusInitiativeProgressInline, StatusInitiativeFinishedInline, StatusInitiativeDoneInline, StatusInitiativeRejectedInline,
    StatusInitiativeHearAdminInline, StatusInitiativeEditingAdminInline, StatusInitiativeProgressAdminInline, StatusInitiativeFinishedAdminInline,
    StatusInitiativeRejectedAdminInline, CommentInline
)

import logging
logger = logging.getLogger(__name__)


class PublicFilter(SimpleListFilter):
    title = _('is publuc')
    parameter_name = 'public'

    def lookups(self, request, model_admin):
        statuses = list(set(list(model_admin.model.objects.all().values_list("initiative_statuses__status__name", flat=True))))
        return [('Public', _('Objavleno')), ('Private', _('Nepregledano'))]

    def queryset(self, request, queryset):
        if self.value() == 'Public':
            return queryset.exclude(Q(initiative_statuses__publication_status=Published.DRAFT) | Q(initiative_statuses__publication_status=None))
        elif self.value() == 'Private':
            return queryset.exclude(initiative_statuses__publication_status=Published.PUBLISHED)
        else:
            return queryset


class InitiativeAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview']
    list_display = [
        'title',
        'reviewer',
        'author',
        'type',
        'zone',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        '_is_published',
        '_needs_publish'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearInline,
        StatusInitiativeEditingInline,
        StatusInitiativeProgressInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeDoneInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = _("Print initiatives")


# ---- ZANIMA ME -> interested in

class InterestedInitiativeSuperAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview']
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
        '_is_published',
        '_needs_publish'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearAdminInline,
        StatusInitiativeFinishedAdminInline,
        StatusInitiativeRejectedAdminInline,
        CommentInline)

    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class InterestedAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        idx = Reviwers.get_order().index(self.instance.reviewer)
        self.fields['reviewer_user'].queryset = User.objects.filter(
            role=Reviwers.get_order()[idx+1],
            area=self.instance.area)


class InterestedInitiativeAreaAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    form = InterestedAdminForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone']
    modifiable = False
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class InterestedInitiativeAppraiserAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'reviewer_user', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    actions = ['printer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        areas = request.user.area.all()
        return qs.filter(area__in=areas)

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"

# ---- IDEJA Idea

class IdeaInitiativeSuperAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview']
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
        '_is_published',
        '_needs_publish'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearAdminInline,
        StatusInitiativeEditingAdminInline,
        StatusInitiativeFinishedAdminInline,
        StatusInitiativeRejectedAdminInline,
        CommentInline)

    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class IteaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        idx = Reviwers.get_order().index(self.instance.reviewer)
        self.fields['reviewer_user'].queryset = User.objects.filter(
            role=Reviwers.get_order()[idx+1],
            area=self.instance.area)

class IdeaInitiativeAreaAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    form = IteaAdminForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone']
    modifiable = False
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearInline,
        StatusInitiativeEditingAdminInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = _("Print initiatives")


class IdeaInitiativeAppraiserAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    form = IteaAdminForm
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeEditingAdminInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    actions = ['printer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        areas = request.user.area.all()
        return qs.filter(area__in=areas)

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class IdeaInitiativeContractorAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'reviewer_user', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    actions = ['printer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(reviewer_user=request.user)

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


# MOTI ME -> bothers me

class BothersInitiativeSuperAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview']
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
        '_is_published',
        '_needs_publish'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearAdminInline,
        StatusInitiativeEditingAdminInline,
        StatusInitiativeFinishedAdminInline,
        StatusInitiativeRejectedAdminInline,
        CommentInline)

    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class BothersInitiativeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        idx = Reviwers.get_order().index(self.instance.reviewer)
        self.fields['reviewer_user'].queryset = User.objects.filter(
            role=Reviwers.get_order()[idx+1],
            area=self.instance.area)


class BothersInitiativeAreaAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    form = BothersInitiativeForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone']
    modifiable = False
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearInline,
        StatusInitiativeEditingInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class BothersInitiativeAppraiserAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    form = BothersInitiativeForm
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeEditingInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    actions = ['printer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        areas = request.user.area.all()
        return qs.filter(area__in=areas)

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class BothersInitiativeContractorAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'reviewer_user', 'reviewer']
    modifiable = False
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    list_display = [
        'title',
        'author',
        'type',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    actions = ['printer']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(reviewer_user=request.user)

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


admin.site.register(Initiative, InitiativeAdmin)
admin.site.register(ArchivedInitiative)

admin.site.register(InterestedInitiativeSuper, InterestedInitiativeSuperAdmin)
admin.site.register(InterestedInitiativeArea, InterestedInitiativeAreaAdmin)
admin.site.register(InterestedInitiativeAppraiser, InterestedInitiativeAppraiserAdmin)

admin.site.register(IdeaInitiativeSuper, IdeaInitiativeSuperAdmin)
admin.site.register(IdeaInitiativeArea, IdeaInitiativeAreaAdmin)
admin.site.register(IdeaInitiativeAppraiser, IdeaInitiativeAppraiserAdmin)
admin.site.register(IdeaInitiativeContractor, IdeaInitiativeContractorAdmin)

admin.site.register(BothersInitiativeSuper, BothersInitiativeSuperAdmin)
admin.site.register(BothersInitiativeArea, BothersInitiativeAreaAdmin)
admin.site.register(BothersInitiativeAppraiser, BothersInitiativeAppraiserAdmin)
admin.site.register(BothersInitiativeContractor, BothersInitiativeContractorAdmin)
