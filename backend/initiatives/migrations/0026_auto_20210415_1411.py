# Generated by Django 3.1.5 on 2021-04-15 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0025_auto_20210415_1354"),
    ]

    operations = [
        migrations.AlterField(
            model_name="description",
            name="title",
            field=models.CharField(max_length=1024, verbose_name="Description title"),
        ),
    ]
