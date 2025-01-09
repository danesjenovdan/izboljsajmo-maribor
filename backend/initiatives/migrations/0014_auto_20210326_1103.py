# Generated by Django 3.1.5 on 2021-03-26 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0013_auto_20210325_1239"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="name",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Display name"
            ),
        ),
        migrations.AlterField(
            model_name="initiative",
            name="cover_image",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="initiative_before",
                to="initiatives.image",
                verbose_name="Cover image before",
            ),
        ),
        migrations.AlterField(
            model_name="initiative",
            name="cover_image_after",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="initiative_after",
                to="initiatives.image",
                verbose_name="Cover image after",
            ),
        ),
    ]
