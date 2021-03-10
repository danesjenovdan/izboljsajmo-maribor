from django.contrib import admin

# Register your models here.

from initiatives.models import (
    Initiative, BothersInitiativeSuper, BothersInitiativeArea, BothersInitiativeContractor,
    IdeaInitiative,
    InterestedInitiative
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
    list_display = [
        'title',
        'reviwer',
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


class BothersInitiativeSuperAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
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
        StatusInitiativeHearAdminInline,
        StatusInitiativeFinishedAdminInline,
        StatusInitiativeRejectedAdminInline,
        CommentInline)

    resource_class = InitiativeResource


class BothersInitiativeAreaAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
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
        StatusInitiativeHearInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    resource_class = InitiativeResource


class BothersInitiativeContractorAdmin(ImportExportModelAdmin):
    readonly_fields = ['title', 'author', 'address', 'type', 'area', 'location', 'cover_image', 'zone', 'modified', 'archived']
    exclude = ['publisher', ]
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['area', 'zone']
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


class IdeaInitiativeAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
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
        StatusInitiativeHearInline,
        StatusInitiativeEditingInline,
        StatusInitiativeProgressInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeDoneInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    resource_class = InitiativeResource


class InterestedInitiativeAdmin(ImportExportModelAdmin):
    search_fields = ['author__username', 'address', 'descriptions__content']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
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
        StatusInitiativeHearInline,
        StatusInitiativeEditingInline,
        StatusInitiativeProgressInline,
        StatusInitiativeFinishedInline,
        StatusInitiativeDoneInline,
        StatusInitiativeRejectedInline,
        CommentInline)

    resource_class = InitiativeResource


#admin.site.register(Initiative, InitiativeAdmin)
admin.site.register(BothersInitiativeSuper, BothersInitiativeSuperAdmin)
admin.site.register(BothersInitiativeArea, BothersInitiativeAreaAdmin)
admin.site.register(BothersInitiativeContractor, BothersInitiativeContractorAdmin)

admin.site.register(IdeaInitiative, IdeaInitiativeAdmin)
admin.site.register(InterestedInitiative, InterestedInitiativeAdmin)
