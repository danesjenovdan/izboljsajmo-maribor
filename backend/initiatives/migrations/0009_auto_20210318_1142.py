# Generated by Django 3.1.5 on 2021-03-18 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0008_superadminuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='initiative',
            name='reviewer_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed', to=settings.AUTH_USER_MODEL, verbose_name='Reviewer'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='reviewer',
            field=models.CharField(choices=[('SA', 'SUPER ADMIN'), ('AA', 'AREA ADMIN'), ('AP', 'AREA APPRAISER'), ('CA', 'CONTRACTOR APPRAISER')], default='AA', max_length=2, verbose_name='Reviewer role'),
        ),
    ]
