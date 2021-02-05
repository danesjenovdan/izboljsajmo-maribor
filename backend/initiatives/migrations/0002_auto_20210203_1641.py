# Generated by Django 3.1.5 on 2021-02-03 16:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='Status_initiative',
        ),
        migrations.AddField(
            model_name='file',
            name='status_initiative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='initiatives.statusinitiative', verbose_name='Status Initiative'),
        ),
        migrations.AlterField(
            model_name='file',
            name='initiative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='initiatives.initiative', verbose_name='Initiative'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+ -]+$', 'Enter a valid username.', 'invalid')], verbose_name='username'),
        ),
    ]