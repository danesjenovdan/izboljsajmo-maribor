# Generated by Django 3.1.5 on 2021-06-02 15:50

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0027_auto_20210602_1233"),
    ]

    operations = [
        migrations.AlterField(
            model_name="initiative",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=3857
            ),
        ),
    ]
