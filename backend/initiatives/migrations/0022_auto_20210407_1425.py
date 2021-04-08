# Generated by Django 3.1.5 on 2021-04-07 14:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0021_auto_20210407_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='for_area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='initiatives.area', verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='for_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL, verbose_name='Uporabnik'),
        ),
    ]