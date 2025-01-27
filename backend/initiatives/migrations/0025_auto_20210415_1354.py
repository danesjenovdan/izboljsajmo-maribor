# Generated by Django 3.1.5 on 2021-04-15 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0024_auto_20210413_1817"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="description",
            options={
                "ordering": ["order"],
                "verbose_name": "Opis",
                "verbose_name_plural": "Opisi",
            },
        ),
        migrations.AddField(
            model_name="initiative",
            name="is_social_inovative_idea",
            field=models.BooleanField(
                default=False, verbose_name="Is social inovative idea"
            ),
        ),
    ]
