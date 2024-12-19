import ogr
import osr
import requests
from django.contrib.gis.geos import Polygon
from django.core.management.base import BaseCommand, CommandError
from initiatives.models import Address, Zone


class Command(BaseCommand):
    help = "Setup data for development"

    def handle(self, *args, **options):

        url = "https://prostor.maribor.si/ows/public/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=public:gurs_izv_ren_stavbe_naslovi&outputFormat=json"
        data = requests.get(url).json()
        for features in data["features"]:
            address = features["properties"]["naslov"]

            Address(name=address).save()
