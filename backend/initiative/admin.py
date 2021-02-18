from django.contrib import admin

# Register your models here.

from .models import (
    Initiative, BothersInitiative, IdeaInitiative, InterestedInitiative
)

from initiatives.admin import (DescriptionInline, FileInline, StatusInitiativeHearInline, StatusInitiativeEditingInline,
    StatusInitiativeProgressInline, StatusInitiativeFinishedInline, StatusInitiativeDoneInline, StatusInitiativeRejectedInline,
    CommentInline
)

from .export_resources import InitiativeResource
from import_export.admin import ImportExportModelAdmin


class InitiativeAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone', 'area', 'type']
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


class BothersInitiativeAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone', 'area', 'type']
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


class IdeaInitiativeAdmin(ImportExportModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone', 'area', 'type']
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
    search_fields = ['name']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
    list_filter = ['statuses', 'zone', 'area', 'type']
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
admin.site.register(BothersInitiative, BothersInitiativeAdmin)
admin.site.register(IdeaInitiative, IdeaInitiativeAdmin)
admin.site.register(InterestedInitiative, InterestedInitiativeAdmin)
