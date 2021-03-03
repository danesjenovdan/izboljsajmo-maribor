from import_export import resources
from .models import Initiative

class InitiativeResource(resources.ModelResource):

    class Meta:
        model = Initiative
        fields = ['type', 'title', 'status', 'area', 'zone', 'publisher', 'created', 'author']
