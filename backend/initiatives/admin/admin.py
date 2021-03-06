from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from django.utils.html import format_html
from django.urls import reverse

from initiatives.models import (
    User, BasicUser, SuperAdminUser, AreaAdminUser, AreaAppraiserUser, ContractorAppraiserUser, Organization, Zone, CompetentService,
    Area, Status, StatusInitiative, File, Comment, Comment, FAQ, StatusInitiativeHear, Rejection, Image,
    StatusInitiativeHear, StatusInitiativeEditing, StatusInitiativeProgress,
    StatusInitiativeFinished, StatusInitiativeDone, StatusInitiativeRejected, Description, Notification
)
from initiatives.forms import (
    HearStatusInlineForm, EditingStatusInlineForm, ProgressStatusInlineForm, DoneStatusInlineForm,
    FinishedStatusInlineForm, RejectedStatusInlineForm
)

from admin_ordering.admin import OrderableAdmin


class BasicUserAdmin(UserAdmin):
    search_fields = ['username']
    autocomplete_fields = ['zones', 'organizations', 'competent_services']
    list_display = [
        'username',
        'created',
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'email_confirmed', 'blocked'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('MB datas'), {'fields': ('role', 'zones', 'organizations', 'competent_services', 'area', 'phone_number')}),
        (_('Notes'), {'fields': ('note',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


class MBUserAdmin(UserAdmin):
    search_fields = ['username']
    autocomplete_fields = ['zones', 'organizations', 'competent_services']
    list_display = [
        'username',
        'created',
    ]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'email_confirmed'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('MB datas'), {'fields': ('role', 'zones', 'organizations', 'competent_services', 'area', 'phone_number')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

class EmptyUserAdmin(UserAdmin):
    fieldsets = []


class SuperAdminUserAdmin(MBUserAdmin):
    readonly_fields = ['role']


class AreaAdminUserAdmin(MBUserAdmin):
    readonly_fields = ['role']


class AreaAppraiserUserAdmin(MBUserAdmin):
    readonly_fields = ['role']


class ContractorAppraiserUserAdmin(MBUserAdmin):
    readonly_fields = ['role']


class UserOrganizationInline(admin.TabularInline):
    model = User.organizations.through
    autocomplete_fields = ['user']
    extra = 1


class UserZoneInline(admin.TabularInline):
    model = User.zones.through
    autocomplete_fields = ['user']
    extra = 1


class UserCompetentServiceInline(admin.TabularInline):
    model = User.competent_services.through
    autocomplete_fields = ['user']
    extra = 1


class CommentInline(admin.TabularInline):
    readonly_fields = ['author', 'created']
    classes = ['collapse']
    fields = ['author', 'content', 'created', 'status']
    model = Comment
    extra = 0


class StatusInitiativeInline(admin.TabularInline):
    readonly_fields = []
    classes = ['collapse']
    fields = ['status', 'note', 'email_content', 'reason_for_rejection', 'competent_service']
    model = StatusInitiative
    extra = 0


class StatusInitiativeHearInline(admin.TabularInline):
    form = HearStatusInlineForm
    readonly_fields = ['status', 'created']
    fields = ['status', 'created', 'email_content']
    classes = ['collapse']
    model = StatusInitiativeHear
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.status = Status.objects.get(name='Slišimo')
        super().save_model(request, obj, form, change)


class StatusInitiativeHearAdminInline(StatusInitiativeHearInline):
    fields = ['status', 'created', 'email_content', 'publication_status']


class StatusInitiativeEditingInline(admin.TabularInline):
    form = EditingStatusInlineForm
    readonly_fields = ['created']
    autocomplete_fields = ['competent_service']
    fields = ['created', 'email_content', 'competent_service']
    classes = ['collapse']
    model = StatusInitiativeEditing
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.status = Status.objects.get(name='Urejamo')
        super().save_model(request, obj, form, change)


class StatusInitiativeEditingAdminInline(StatusInitiativeEditingInline):
    fields = ['created', 'email_content', 'competent_service', 'publication_status']


class StatusInitiativeProgressInline(admin.TabularInline):
    form = ProgressStatusInlineForm
    readonly_fields = ['created']
    fields = ['created', 'email_content']
    classes = ['collapse']
    model = StatusInitiativeProgress
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.status = Status.objects.get(name='V izvajanju')
        super().save_model(request, obj, form, change)


class StatusInitiativeProgressAdminInline(StatusInitiativeProgressInline):
    fields = ['created', 'email_content', 'publication_status']


class StatusInitiativeFinishedInline(admin.TabularInline):
    form = FinishedStatusInlineForm
    readonly_fields = ['created']
    fields = ['created', 'email_content']
    classes = ['collapse']
    model = StatusInitiativeFinished
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.status = Status.objects.get(name='Zaključeno')
        super().save_model(request, obj, form, change)


class StatusInitiativeFinishedAdminInline(StatusInitiativeFinishedInline):
    fields = ['created', 'email_content', 'publication_status']


class StatusInitiativeDoneInline(admin.TabularInline):
    form = DoneStatusInlineForm
    readonly_fields = ['created']
    fields = ['created', 'email_content']
    classes = ['collapse']
    model = StatusInitiativeDone
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.status = Status.objects.get(name='Izvedeno')
        super().save_model(request, obj, form, change)


class StatusInitiativeDoneAdminInline(StatusInitiativeDoneInline):
    fields = ['created', 'email_content', 'publication_status']


class StatusInitiativeRejectedInline(admin.TabularInline):
    form = RejectedStatusInlineForm
    readonly_fields = ['created']
    fields = ['created', 'email_content', 'reason_for_rejection']
    autocomplete_fields = ['reason_for_rejection',]
    classes = ['collapse']
    model = StatusInitiativeRejected
    extra = 0

    def save_model(self, request, obj, form, change):
        obj.status = Status.objects.get(name='Zavrnjeno')
        super().save_model(request, obj, form, change)

    class Media:
        js = (
            'js/rejection_email_content_filler.js',
        )


class StatusInitiativeRejectedAdminInline(StatusInitiativeRejectedInline):
    fields = ['created', 'email_content', 'reason_for_rejection', 'publication_status']

class DescriptionInline(admin.TabularInline):
    search_fields = ['title']
    fields = ['field', 'title', 'content']
    classes = ['collapse']
    model = Description
    extra = 0


class FileInline(admin.TabularInline):
    search_fields = ['name']
    fields = ['name', 'file']
    classes = ['collapse']
    model = File
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        'name',
        'number_of_members',
    ]
    inlines = (UserOrganizationInline, )


class RejectionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        'name',
    ]


class ZoneAdmin(gis_admin.OSMGeoAdmin):
    search_fields = ['name']
    list_display = [
        'name',
    ]
    inlines = (UserZoneInline, )


class CompetentServiceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        'name',
    ]
    inlines = (UserCompetentServiceInline, )


class AreaAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'initiative_obj', "content", "author", "status", 'created']
    list_editable = ["status"]

    list_filter = ['status']

    def initiative_obj(self, obj):
        link = reverse("admin:initiatives_initiative_change", args=[obj.initiative.id])
        return format_html(f'<a href="{link}">{obj.initiative}</a>')

    initiative_obj.allow_tags = True
    initiative_obj.short_description = _('Initiatives')


class FAQAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = ["question", "answer", "order"]
    ordering_field = "order"
    list_editable = ["order"]


admin.site.register(User, EmptyUserAdmin)
admin.site.register(BasicUser, BasicUserAdmin)
admin.site.register(SuperAdminUser, SuperAdminUserAdmin)
admin.site.register(AreaAdminUser, AreaAdminUserAdmin)
admin.site.register(AreaAppraiserUser, AreaAppraiserUserAdmin)
admin.site.register(ContractorAppraiserUser, ContractorAppraiserUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(CompetentService, CompetentServiceAdmin)
admin.site.register(Status)
admin.site.register(StatusInitiative)
admin.site.register(File)
admin.site.register(Image)
admin.site.register(Notification)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FAQ, FAQAdmin)
admin.site.register(Rejection, RejectionAdmin)

admin.site.site_header = _('Izboljšajmo Maribor')
