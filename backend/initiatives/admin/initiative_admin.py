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
        return [('Public', _('Objavljeno')), ('Private', _('Nepregledano'))]

    def queryset(self, request, queryset):
        if self.value() == 'Public':
            return queryset.exclude(Q(initiative_statuses__publication_status=Published.DRAFT) | Q(initiative_statuses__publication_status=None))
        elif self.value() == 'Private':
            return queryset.exclude(initiative_statuses__publication_status=Published.PUBLISHED)
        else:
            return queryset

class InitiativeParentAdmin(gis_admin.OSMGeoAdmin, admin.ModelAdmin):
    def save_formset(self, request, obj, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.author = request.user
            instance.save()
            formset.save()

    actions = ['printer']

    def email(self, obj):
        return obj.author.email

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    def phone_number(self, obj):
        return obj.author.phone_number

    printer.short_description = "Print initiatives"
    phone_number.short_description = _("Telefonska številka")


class InitiativeAdmin(InitiativeParentAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview', 'description']
    list_display = [
        'id',
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

    # WARNING if you add ore remove some inline, you need to edit JS for insert rejection email content. /static_files/js/rejection_email_content_filler.js
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


# ---- ZANIMA ME -> interested in

class InterestedInitiativeSuperAdmin(InitiativeParentAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview', 'phone_number', 'email', 'description']
    exclude = ['is_draft']
    list_display = [
        'id',
        'title',
        'author',
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


class InterestedAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        idx = Reviwers.get_order().index(self.instance.reviewer)
        self.fields['reviewer_user'].queryset = User.objects.filter(
            role=Reviwers.get_order()[idx+1],
            area=self.instance.area)


class InterestedInitiativeAreaAdmin(InitiativeParentAdmin):
    form = InterestedAdminForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone', 'area']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'archived', 'address', 'publisher', 'zone', 'phone_number', 'email', 'description']
    modifiable = False
    exclude = ['is_draft']
    list_display = [
        'id',
        'title',
        'author',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
    ]
    # WARNING if you add ore remove some inline, you need to edit JS for insert rejection email content. /static_files/js/rejection_email_content_filler.js
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeRejectedInline,
        CommentInline)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        areas = request.user.area.all()
        #return qs.filter(area__in=areas)
        #WORKAROUND aggregate() + distinct(fields) not implemented.
        initiatives = qs.filter(Q(reviewer_user_history=request.user) | Q(area__in=areas))
        return qs.filter(id__in=initiatives)



class InterestedInitiativeAppraiserAdmin(InitiativeParentAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'archived', 'address', 'publisher', 'zone', 'reviewer_user', 'reviewer', 'phone_number', 'email', 'description']
    exclude = ['publisher', 'is_draft']
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'id',
        'title',
        'author',
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        areas = request.user.area.all()
        #return qs.filter(area__in=areas)
        #WORKAROUND aggregate() + distinct(fields) not implemented.
        initiatives = qs.filter(Q(reviewer_user_history=request.user) | Q(area__in=areas))
        return qs.filter(id__in=initiatives)


# ---- IDEJA Idea

class IdeaInitiativeSuperAdmin(InitiativeParentAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview', 'phone_number', 'email', 'description']
    exclude = ['is_draft']
    list_display = [
        'id',
        'title',
        'author',
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



class IdeaAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        idx = Reviwers.get_order().index(self.instance.reviewer)
        self.fields['reviewer_user'].queryset = User.objects.filter(
            role=Reviwers.get_order()[idx+1],
            area=self.instance.area)

class IdeaInitiativeAreaAdmin(InitiativeParentAdmin):
    form = IdeaAdminForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone', 'area']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'archived', 'address', 'publisher', 'zone', 'phone_number', 'email', 'description']
    modifiable = False
    exclude = ['is_draft']
    list_display = [
        'id',
        'title',
        'author',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
    ]
    # WARNING if you add ore remove some inline, you need to edit JS for insert rejection email content. /static_files/js/rejection_email_content_filler.js
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearInline,
        StatusInitiativeEditingAdminInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        areas = request.user.area.all()
        #return qs.filter(area__in=areas)
        #WORKAROUND aggregate() + distinct(fields) not implemented.
        initiatives = qs.filter(Q(reviewer_user_history=request.user) | Q(area__in=areas))
        return qs.filter(id__in=initiatives)



class IdeaInitiativeAppraiserAdmin(InitiativeParentAdmin):
    form = IdeaAdminForm
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'archived', 'address', 'publisher', 'zone', 'phone_number', 'email', 'description']
    exclude = ['publisher', 'is_draft']
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'id',
        'title',
        'author',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeEditingInline,
        StatusInitiativeFinishedInline,
        CommentInline)


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        areas = request.user.area.all()
        #return qs.filter(area__in=areas)
        #WORKAROUND aggregate() + distinct(fields) not implemented.
        initiatives = qs.filter(Q(reviewer_user_history=request.user) | Q(area__in=areas))
        return qs.filter(id__in=initiatives)


class IdeaInitiativeContractorAdmin(InitiativeParentAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'archived', 'address', 'publisher', 'zone', 'reviewer_user', 'reviewer', 'phone_number', 'email', 'description']
    exclude = ['publisher', 'is_draft']
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'id',
        'title',
        'author',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeEditingInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(reviewer_user_history=request.user)



# MOTI ME -> bothers me

class BothersInitiativeSuperAdmin(InitiativeParentAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created', 'images_preview', 'phone_number', 'email', 'description']
    exclude = ['is_draft']
    list_display = [
        'id',
        'title',
        'author',
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



class BothersInitiativeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        idx = Reviwers.get_order().index(self.instance.reviewer)
        self.fields['reviewer_user'].queryset = User.objects.filter(
            role__in=Reviwers.get_order()[idx+1:],
            area=self.instance.area)


class BothersInitiativeAreaAdmin(InitiativeParentAdmin):
    form = BothersInitiativeForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['zone', 'area']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'archived', 'address', 'publisher', 'zone', 'phone_number', 'email', 'description', 'description']
    modifiable = False
    exclude = ['is_draft']
    list_display = [
        'id',
        'title',
        'author',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
    ]
    # WARNING if you add ore remove some inline, you need to edit JS for insert rejection email content. /static_files/js/rejection_email_content_filler.js
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearInline,
        StatusInitiativeEditingInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #WORKAROUND aggregate() + distinct(fields) not implemented.
        initiatives = qs.filter(Q(reviewer_user_history=request.user) | Q(area__in=request.user.area.all()))
        return qs.filter(id__in=initiatives)


class BothersInitiativeAppraiserAdmin(InitiativeParentAdmin):
    form = BothersInitiativeForm
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'archived', 'address', 'publisher', 'zone', 'phone_number', 'email', 'description']
    exclude = ['publisher', 'is_draft']
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    modifiable = False
    list_display = [
        'id',
        'title',
        'author',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeEditingInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #WORKAROUND aggregate() + distinct(fields) not implemented.
        initiatives = qs.filter(Q(reviewer_user_history=request.user) | Q(area__in=request.user.area.all()))
        return qs.filter(id__in=initiatives)


class BothersInitiativeContractorAdmin(InitiativeParentAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'archived', 'address', 'publisher', 'zone', 'reviewer_user', 'reviewer', 'phone_number', 'email', 'description']
    modifiable = False
    exclude = ['publisher', 'is_draft']
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type', PublicFilter]
    list_display = [
        'id',
        'title',
        'author',
        'publisher',
        'status',
        'area',
        'zone',
        'created',
        'comment_count',
        'vote_count',
        'reviewer',
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeEditingInline,
        StatusInitiativeFinishedInline,
        CommentInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(reviewer_user_history=request.user)



def get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    ordering = {
        "Pobude": 1,
        "Arhivirane pobude": 2,
        "Pobude zanima me (Superadmin - nivo 1)": 3,
        "Pobude zanima me (Vodja področja - nivo 2)": 4,
        "Pobude zanima me (Skrbnik področja - nivo 3)": 5,
        "Pobude moti me (Superadmin - nivo 1)": 6,
        "Pobude moti me (Vodja področja - nivo 2)": 7,
        "Pobude moti me (Skrbnik področja - nivo 3)": 8,
        "Pobude moti me (Izvajalci - nivo 4)": 9,
        "Pobude imam idejo (Superadmin - nivo 1)": 10,
        "Pobude imam idejo (Vodja področja - nivo 2)": 11,
        "Pobude imam idejo (Skrbnik področja - nivo 3)": 12,
        "Pobude imam idejo (Izvajalec - nivo 4)": 13,
        "Zavrnitve": 14,
        "Slike": 15,
        "Datoteke": 16,
        "Statusi": 17,
        "Statusi pobud": 18,
        "Območja": 19,
        "Področja": 20,
        "Komentarji": 21,
        "Nivo1 Superadmin": 22,
        "Superadmin - nivo 1": "22",
        "Vodje področij - nivo 2": 23,
        "Skrbniki področij - nivo 3": 24,
        "Izvajaleci - nivo 4": 25,
        "Vsi admini": 26,
        "Navadni uporabniki": 27,
        "Uporabniki": 28,
        "Organizacija": 29,
        "Competent services": 30,
        "Naslovi": 31,
        "Obvestila": 32,
        "FAQ": 33,
        "Predogled": 34,
        "Youtube Embed": 35,
        "Naslovi": 36,
        "Naslovi 2": 37,
        "Slike": 38,
        "Vsebine": 39,
        "Skupine": 40,
        "Applications": 41,
        "Grants": 42,
        "Access tokens": 43,
        "Refresh tokens": 44,
        "Intervals": 45,
        "Crontabs": 46,
        "Solar events": 47,
        "Clocked": 48,
        "Periodic tasks": 49,
        "User social auths": 50,
        "Nonces": 51,
        "Associations": 52,
    }
    app_dict = self._build_app_dict(request)
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        print(app['models'])
        app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list

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

admin.site.site_header = _('Izboljšajmo Maribor')

admin.AdminSite.get_app_list = get_app_list
