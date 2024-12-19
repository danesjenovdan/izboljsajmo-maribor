from admin_ordering.admin import OrderableAdmin
from django.contrib import admin
from django.utils.translation import gettext as _

from .models import (
    About,
    AboutContent,
    AboutImage,
    AboutTitle,
    AboutTitle2,
    AboutType,
    AboutYoutubeEmbed,
)


class AboutAdmin(OrderableAdmin, admin.ModelAdmin):
    ordering_field = "order"

    list_display = ["description", "order", "preview"]
    list_editable = ["order"]

    ordering = ("order",)

    def get_fieldsets(self, request, obj=None):
        """
        Different fieldset for the admin form
        """
        self.fieldsets = (
            self.dynamic_fieldset()
        )  # add logic to add the dynamic fieldset with fields
        return super().get_fieldsets(request, obj)

    def dynamic_fieldset(self):
        """
        get the dynamic field sets
        """
        sections = {
            "Global": ["type", "order", "description"],
            "Titles, Text": ["content", "description"],
            "Youtube, Image": ["url"],
            "Image": ["image"],
        }
        fieldsets = []
        for group in sections.keys():  # logic to get the field set group
            fields = []
            for field in sections[group]:  # logic to get the group fields
                fields.append(field)

            fieldset_values = {"fields": tuple(fields), "classes": []}
            fieldsets.append((group, fieldset_values))

        fieldsets = tuple(fieldsets)

        return fieldsets


class AboutYoutubeEmbedAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = ["description", "order", "preview"]
    fieldsets = ((None, {"fields": ("url", "description")}),)

    def save_model(self, request, obj, form, change):
        obj.type = AboutType.YOUTUBE_EMBED
        super().save_model(request, obj, form, change)


class AboutTitleAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = ["description", "order", "preview"]
    fieldsets = ((None, {"fields": ("content", "description")}),)

    def save_model(self, request, obj, form, change):
        obj.type = AboutType.TITLE
        super().save_model(request, obj, form, change)


class AboutTitle2Admin(OrderableAdmin, admin.ModelAdmin):
    list_display = ["description", "order", "preview"]
    fieldsets = ((None, {"fields": ("content", "description")}),)

    def save_model(self, request, obj, form, change):
        obj.type = AboutType.TITLE2
        super().save_model(request, obj, form, change)


class AboutImageAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = ["description", "order", "preview"]
    fieldsets = ((None, {"fields": ("url", "image", "description")}),)

    def save_model(self, request, obj, form, change):
        obj.type = AboutType.IMAGE
        super().save_model(request, obj, form, change)


class AboutContentAdmin(OrderableAdmin, admin.ModelAdmin):
    list_display = ["description", "order", "preview"]
    fieldsets = ((None, {"fields": ("content", "description")}),)

    def save_model(self, request, obj, form, change):
        obj.type = AboutType.TEXT
        super().save_model(request, obj, form, change)


admin.site.register(About, AboutAdmin)
admin.site.register(AboutYoutubeEmbed, AboutYoutubeEmbedAdmin)
admin.site.register(AboutTitle, AboutTitleAdmin)
admin.site.register(AboutTitle2, AboutTitle2Admin)
admin.site.register(AboutImage, AboutImageAdmin)
admin.site.register(AboutContent, AboutContentAdmin)
