from django.contrib import admin

# Register your models here.

from initiatives.models import (
    Initiative, BothersInitiativeSuper, BothersInitiativeArea, BothersInitiativeAppraiser, BothersInitiativeContractor,
    IdeaInitiativeSuper, IdeaInitiativeArea, IdeaInitiativeAppraiser, IdeaInitiativeContractor,
    InterestedInitiativeSuper, InterestedInitiativeArea, InterestedInitiativeAppraiser,
    ArchivedInitiative
)

from initiatives.admin.admin import (DescriptionInline, FileInline, StatusInitiativeHearInline, StatusInitiativeEditingInline,
    StatusInitiativeProgressInline, StatusInitiativeFinishedInline, StatusInitiativeDoneInline, StatusInitiativeRejectedInline,
    StatusInitiativeHearAdminInline, StatusInitiativeEditingAdminInline, StatusInitiativeProgressAdminInline, StatusInitiativeFinishedAdminInline,
    StatusInitiativeRejectedAdminInline, CommentInline
)

from initiatives.export_resources import InitiativeResource
from import_export.admin import ImportExportModelAdmin


class InitiativeAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created']
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
        'vote_count'
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


# ---- ZANIMA ME -> interested in

class InterestedInitiativeSuperAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created']
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
        'reviewer'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearAdminInline,
        StatusInitiativeFinishedAdminInline,
        StatusInitiativeRejectedAdminInline,
        CommentInline)

    resource_class = InitiativeResource


class InterestedInitiativeAreaAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created']
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


class InterestedInitiativeAppraiserAdmin(ImportExportModelAdmin):
    readonly_fields = ['title', 'author', 'address', 'type', 'area', 'location', 'cover_image', 'zone', 'modified', 'archived', 'status_history', 'created']
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

# ---- IDEJA Idea

class IdeaInitiativeSuperAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created']
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
        'reviewer'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearAdminInline,
        StatusInitiativeFinishedAdminInline,
        StatusInitiativeRejectedAdminInline,
        CommentInline)

    resource_class = InitiativeResource


class IdeaInitiativeAreaAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created']
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


class IdeaInitiativeAppraiserAdmin(ImportExportModelAdmin):
    readonly_fields = ['title', 'author', 'address', 'type', 'area', 'location', 'cover_image', 'zone', 'modified', 'archived', 'status_history', 'created']
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


class IdeaInitiativeContractorAdmin(ImportExportModelAdmin):
    readonly_fields = ['title', 'author', 'address', 'type', 'area', 'location', 'cover_image', 'zone', 'modified', 'archived', 'status_history', 'created']
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


# MOTI ME -> bothers me

class BothersInitiativeSuperAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created']
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
        'reviewer'
    ]
    inlines = (
        DescriptionInline,
        FileInline,
        StatusInitiativeHearAdminInline,
        StatusInitiativeFinishedAdminInline,
        StatusInitiativeRejectedAdminInline,
        CommentInline)

    resource_class = InitiativeResource


class BothersInitiativeAreaAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
    list_filter = ['statuses', 'zone__name', 'area__name', 'type']
    date_hierarchy = 'created'
    readonly_fields = ['status_history', 'created']
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


class BothersInitiativeAppraiserAdmin(ImportExportModelAdmin):
    readonly_fields = ['title', 'author', 'address', 'type', 'area', 'location', 'cover_image', 'zone', 'modified', 'archived', 'status_history', 'created']
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


class BothersInitiativeContractorAdmin(ImportExportModelAdmin):
    readonly_fields = ['title', 'author', 'address', 'type', 'area', 'location', 'cover_image', 'zone', 'modified', 'archived', 'status_history', 'created']
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


admin.site.register(Initiative)
admin.site.register(ArchivedInitiative, InitiativeAdmin)

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
