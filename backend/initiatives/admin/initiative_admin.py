from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.contrib.gis import admin as gis_admin

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

from initiatives.export_resources import InitiativeResource
from import_export.admin import ImportExportModelAdmin



class InitiativeAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


# ---- ZANIMA ME -> interested in

class InterestedInitiativeSuperAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
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


class InterestedInitiativeAreaAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    form = InterestedAdminForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class InterestedInitiativeAppraiserAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft', 'reviewer_user', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"

# ---- IDEJA Idea

class IdeaInitiativeSuperAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
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

class IdeaInitiativeAreaAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    form = IteaAdminForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class IdeaInitiativeAppraiserAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    form = IteaAdminForm
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class IdeaInitiativeContractorAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft', 'reviewer_user', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


# MOTI ME -> bothers me

class BothersInitiativeSuperAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone', 'reviewer_user']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
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


class BothersInitiativeAreaAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    form = BothersInitiativeForm
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class BothersInitiativeAppraiserAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    form = BothersInitiativeForm
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft', 'reviewer']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
    actions = ['printer']

    def printer(self, request, queryset):
        return render(request, 'print/initiatives.html', {'initiatives': queryset})

    printer.short_description = "Print initiatives"


class BothersInitiativeContractorAdmin(gis_admin.OSMGeoAdmin, ImportExportModelAdmin):
    readonly_fields = ['title', 'type', 'status_history', 'created', 'images_preview', 'author', 'modified', 'area', 'cover_image', 'archived', 'address', 'publisher', 'zone', 'is_draft', 'reviewer_user', 'reviewer']
    modifiable = False
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    date_hierarchy = 'created'
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
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

    resource_class = InitiativeResource
    actions = ['printer']

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
