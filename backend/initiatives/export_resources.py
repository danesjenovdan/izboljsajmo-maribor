from behaviors.models import Published
from import_export import resources

from .models import Initiative


class InitiativeResource(resources.ModelResource):

    class Meta:
        model = Initiative
        fields = [
            "id",
            "type",
            "title",
            "status",
            "area",
            "zone",
            "created",
            "author",
            "published_at",
        ]
        import_id_fields = ("id", "initiative_statuses__id")
        widgets = {
            "published_at": {"format": "%d.%m.%Y"},
            "created": {"format": "%d.%m.%Y"},
        }

    def dehydrate_published_at(self, obj):
        try:
            date = (
                obj.initiative_statuses.filter(publication_status=Published.PUBLISHED)
                .earliest("created_at")
                .created
            )
        except:
            date = ""
        return date
