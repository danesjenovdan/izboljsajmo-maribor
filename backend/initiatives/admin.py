from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from .models import (
    User, Organization, Zone, CompetentService, Initiative, Area, Status, StatusInitiative,
    File, Comment
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
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('MB datas'), {'fields': ('zones', 'organizations', 'competent_services', 'phone_number')}),
        (_('Notes'), {'fields': ('note',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


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
    fields = ['author', 'content', 'created', 'status']
    model = Comment
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = [
        'name',
        'number_of_members',
    ]
    inlines = (UserOrganizationInline, )


class ZoneAdmin(gis_admin.GeoModelAdmin):
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


class InitiativeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    autocomplete_fields = ['author', 'publisher', 'area', 'zone']
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
    inlines = (CommentInline, )


admin.site.register(Initiative, InitiativeAdmin)
admin.site.register(User, MBUserAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(CompetentService, CompetentServiceAdmin)
admin.site.register(Status)
admin.site.register(StatusInitiative)
admin.site.register(File)
