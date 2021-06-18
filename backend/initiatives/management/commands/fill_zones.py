from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import Polygon

from initiatives.models import Zone

import requests
import ogr, osr

class Command(BaseCommand):
    help = 'Setup data for development'

    def handle(self, *args, **options):

        url = 'https://prostor.maribor.si/ows/public/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=public:gurs_rpe_odo_ck_cm_cv&outputFormat=json'
        data = requests.get(url).json()
        for zone in data['features']:
            data = []
            for coordinates in zone['geometry']['coordinates'][0][0]:
                pointX, pointY = self.projection(coordinates[0], coordinates[1])
                data.append((pointX, pointY))

            poly = Polygon(data)

            name = zone['properties']['odo_uime']

            zone = Zone.objects.filter(name=name)
            if zone:
                zone = zone[0]
                zone.polygon = poly
                zone.save()
            else:
                Zone(
                    name=name,
                    polygon=poly
                ).save()
                # TODO

    def projection(self, pointX, pointY):
        inputEPSG = 3794
        outputEPSG = 4326
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(pointX, pointY)

        # create coordinate transformation
        inSpatialRef = osr.SpatialReference()
        inSpatialRef.ImportFromEPSG(inputEPSG)

        outSpatialRef = osr.SpatialReference()
        outSpatialRef.ImportFromEPSG(outputEPSG)

        coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)

        # transform point
        point.Transform(coordTransform)

        # print point in EPSG 4326
        return point.GetX(), point.GetY()

