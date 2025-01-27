# Generated by Django 3.1.5 on 2021-03-20 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("initiatives", "0009_auto_20210318_1142"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="area",
            field=models.ManyToManyField(
                blank=True,
                related_name="users",
                to="initiatives.Area",
                verbose_name="Area",
            ),
        ),
    ]
