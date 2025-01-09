# Generated by Django 3.1.5 on 2021-03-29 07:57

import initiatives.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0014_auto_20210326_1103"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="file",
            field=models.FileField(
                upload_to="files",
                validators=[initiatives.utils.validate_file_extension],
                verbose_name="File",
            ),
        ),
        migrations.AlterField(
            model_name="statusinitiative",
            name="email_content",
            field=models.TextField(
                blank=True, null=True, verbose_name="Email response"
            ),
        ),
        migrations.AlterField(
            model_name="statusinitiative",
            name="note",
            field=models.TextField(
                blank=True, null=True, verbose_name="Note of status"
            ),
        ),
    ]
