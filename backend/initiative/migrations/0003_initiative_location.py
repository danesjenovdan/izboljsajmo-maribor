# Generated by Django 3.1.5 on 2021-02-18 16:24

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('initiative', '0002_auto_20210218_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(0.0 0.0)', srid=4326),
        ),
    ]
